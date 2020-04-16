##**********************************************
#ATTENTION: This file does not claim to be written by anyone in this project.
#This is used to simply read and utilize the binary that was generated in a proprietary formatting.
#The original code was retrieved from https://github.com/kamalkraj/BERT-NER
#This is simply being used to take the generated binary and make it usable in the context of this project.
##**********************************************

from __future__ import absolute_import, division, print_function

import torch
import torch.nn.functional as F
from pytorch_transformers import (WEIGHTS_NAME, AdamW, BertConfig,
                                  BertForTokenClassification, BertTokenizer,
                                  WarmupLinearSchedule)
from torch import nn
from torch.utils.data import (DataLoader, RandomSampler, SequentialSampler,
                              TensorDataset)
from tqdm import tqdm, trange

#get the abstracted classes from the other file
from RNN_structure import Ner, NerProcessor, InputExample, InputFeatures



##--------------function that converts raw text into masked data the binary will use to predict labels-----------
def convert_examples_to_features(examples, label_list, max_seq_length, tokenizer):
    """Loads a data file into a list of `InputBatch`s."""

    label_map = {label : i for i, label in enumerate(label_list,1)}

    features = []
    for (ex_index,example) in enumerate(examples): #for each example/sentence, mask, predict labels and map the results together
        textlist = example.text_a.split(' ')
        labellist = example.label
        tokens = []
        labels = []
        valid = []
        label_mask = []
        
        origWords = []
        
        for i, word in enumerate(textlist):
            #unmasked words
            origWords.append(word) #save the original (unmasked) word
            token = tokenizer.tokenize(word)
            tokens.extend(token)
            label_1 = labellist[i]
            for m in range(len(token)):
                #only have 1 label/mask for each word
                if m == 0:
                    labels.append(label_1)
                    valid.append(1)
                    label_mask.append(1)
                else:
                    valid.append(0) 
        #masked words
        if len(tokens) >= max_seq_length - 1:
            tokens = tokens[0:(max_seq_length - 2)]
            labels = labels[0:(max_seq_length - 2)]
            valid = valid[0:(max_seq_length - 2)]
            label_mask = label_mask[0:(max_seq_length - 2)]
        ntokens = []
        segment_ids = []
        label_ids = []
        ntokens.append("[CLS]")
        segment_ids.append(0)
        valid.insert(0,1)
        label_mask.insert(0,1)
        label_ids.append(label_map["[CLS]"])
        for i, token in enumerate(tokens):
            ntokens.append(token)
            segment_ids.append(0)
            if len(labels) > i:
                label_ids.append(label_map[labels[i]])
        ntokens.append("[SEP]")
        segment_ids.append(0)
        valid.append(1)
        label_mask.append(1)
        label_ids.append(label_map["[SEP]"])
        input_ids = tokenizer.convert_tokens_to_ids(ntokens) 
        input_mask = [1] * len(input_ids)
        label_mask = [1] * len(label_ids)
        while len(input_ids) < max_seq_length:
            input_ids.append(0)
            input_mask.append(0)
            segment_ids.append(0)
            label_ids.append(0)
            valid.append(1)
            label_mask.append(0)
        while len(label_ids) < max_seq_length:
            label_ids.append(0)
            label_mask.append(0)
        assert len(input_ids) == max_seq_length
        assert len(input_mask) == max_seq_length
        assert len(segment_ids) == max_seq_length
        assert len(label_ids) == max_seq_length
        assert len(valid) == max_seq_length
        assert len(label_mask) == max_seq_length
        #send back all of the data for each example/sentence (all masked text, unmasked text, labels, etc)
        features.append(
                InputFeatures(input_ids=input_ids,
                              input_mask=input_mask,
                              segment_ids=segment_ids,
                              label_id=label_ids,
                              valid_ids=valid,
                              label_mask=label_mask,
                              origWords = origWords))
    return features


###------------------ function that takes the article body and splits it into WORD\nWORD\n... and initializes labels------------------
def readArticle(articleBody):
    data = []
    sentence = []
    label= []
    for sent in articleBody:  #for each sentence
        splits = sent.split(' ') #split it by spaces
        for word in splits: #for each word
            sentence.append(word.upper()) #convert to upper case (sentence array holds ['WORD','WORD',...])
            label.append("O") #all labels are "O" or essentially blank to begin with-- these will change with the prediction
        data.append((sentence,label)) #attach each 
        sentence = []
        label = []

    if len(sentence) >0: #if the sentence array exists
        data.append((sentence,label)) #attach the sentence array and the label array together
        sentence = []
        label = []
    return data #return the words and initial labels

###---------------------------------------------------------------------------------------------------------------


###--------------function that takes article body and returns array of chemicals----------------------------
def readBinary(articleBody):
    processor = NerProcessor() #initialize an NerProcessor class object
    device = torch.device("cpu") #restrict processing to CPU only (GPU only works with NVIDIA GPUs)

    model = Ner.from_pretrained("./out_base") #load in the binary from the directory given
    tokenizer = BertTokenizer.from_pretrained("./out_base") #load in the presets saved

    model.to(device)

#Give the model the set of all labels it will predict, along with the masks it will use
    label_list = ["O", "B-chem", "I-chem", "B-quant", "I-quant", "[CLS]", "[SEP]"]
            
    eval_examples = processor.get_examples(articleBody) #convert article body into words and label arrays
    eval_features = convert_examples_to_features(eval_examples, label_list, 128, tokenizer) #convert words and labels into masked outputs

#seperate out the masked data from the conversion
    all_input_ids = torch.tensor([f.input_ids for f in eval_features], dtype=torch.long)
    all_input_mask = torch.tensor([f.input_mask for f in eval_features], dtype=torch.long)
    all_segment_ids = torch.tensor([f.segment_ids for f in eval_features], dtype=torch.long)
    all_label_ids = torch.tensor([f.label_id for f in eval_features], dtype=torch.long)
    all_valid_ids = torch.tensor([f.valid_ids for f in eval_features], dtype=torch.long)
    all_lmask_ids = torch.tensor([f.label_mask for f in eval_features], dtype=torch.long)
    eval_data = TensorDataset(all_input_ids, all_input_mask, all_segment_ids, all_label_ids,all_valid_ids,all_lmask_ids)
    words = [f.origWords for f in eval_features]

# Run prediction for full data
    eval_sampler = SequentialSampler(eval_data)
    eval_dataloader = DataLoader(eval_data, sampler=eval_sampler, batch_size=8)


    model.eval()
    eval_loss, eval_accuracy = 0, 0
    nb_eval_steps, nb_eval_examples = 0, 0

    y_true = []
    y_pred = []
    label_map = {i : label for i, label in enumerate(label_list,1)}

#populate the prediction arrays for the labels
#look at the word and predict the label for it depending on the model (store the predicted value in y_pred)
    for input_ids, input_mask, segment_ids, label_ids,valid_ids,l_mask in tqdm(eval_dataloader, desc="\nEvaluating"):
        input_ids = input_ids.to(device)
        input_mask = input_mask.to(device)
        segment_ids = segment_ids.to(device)
        valid_ids = valid_ids.to(device)
        label_ids = label_ids.to(device)
        l_mask = l_mask.to(device)

        with torch.no_grad():
            logits = model(input_ids, segment_ids, input_mask,valid_ids=valid_ids,attention_mask_label=l_mask)

        logits = torch.argmax(F.log_softmax(logits,dim=2),dim=2)
        logits = logits.detach().cpu().numpy()
        label_ids = label_ids.to('cpu').numpy()
        input_mask = input_mask.to('cpu').numpy()

        for i, label in enumerate(label_ids):
            temp_1 = []
            temp_2 = []
            for j,m in enumerate(label):
                if j == 0:
                    continue
                elif label_ids[i][j] == len(label_map):
                    y_true.append(temp_1)
                    y_pred.append(temp_2)
                    break
                else:
                    temp_1.append(label_map[label_ids[i][j]])
                    temp_2.append(label_map[logits[i][j]])

#Make predictions for the labels
    chemicals = []
    for i in range(len(y_pred)): #for each predicted sentence
        phrase = ""
        for j in range(len(y_pred[i])): #for each predicted word
            
            if('chem' in y_pred[i][j]): #if the predicted label was a chemical
                
                if j!=(len(y_pred[i])-1) and 'I-' in y_pred[i][j+1]: #if there is a chemical following this one
                    phrase=phrase+words[i][j]+" " #make this chemical the beginning of a phrase (like sodium in "sodium bicarbonate")
                    
                elif j==(len(y_pred[i])-1) or "I-" in y_pred[i][j]: #if this current word is predicted to be in the middle/end of a phrase
                    if j!=(len(y_pred[i])-1) and "I-" in y_pred[i][j+1]: #if this is the middle word (there is another word in the phrase)
                        phrase=phrase+words[i][j]+" " #add this to the phrase
                    else: #if this is the end of a chemical phrase
                        phrase=phrase+words[i][j] #add this chemical word to the phrase
                        chemicals.append(phrase) #add the full chemical phrase to the array
                        phrase = "" #reset the phrase

                elif j==(len(y_pred[i])-1) or 'B-' in y_pred[i][j+1] or 'O' in y_pred[i][j+1]: #if this is the first/last word in the phrase
                    phrase=phrase+words[i][j] #add this chemical word to the phrase
                    chemicals.append(phrase) #add the full chemical phrase to the array
                    phrase = "" #reset the phrase

    bad_chars = [',', '”', ',', '"', "'", ")", "("] #these often are placed in the chemicals when the parsing isn't done correctly
    for chem in chemicals: #for each chemical
        for c in bad_chars:
            if c in chem: #if a bad character is in the chemical phrase
                #remove and replace with the phrase with no bad chars
                try:
                    chemicals.remove(chem)
                except:
                    chemicals.append(chem.replace(c, ''))
                chemicals.append(chem.replace(c, ''))

    #make it into a set to remove all duplicates
    chemicals = list(set(chemicals))

    return chemicals #return the final array
    

###_----------------------------------------------------------------------------------------------



                            
