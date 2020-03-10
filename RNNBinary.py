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

class Ner(BertForTokenClassification):

    def forward(self, input_ids, token_type_ids=None, attention_mask=None, labels=None,valid_ids=None,attention_mask_label=None):
        sequence_output = self.bert(input_ids, token_type_ids, attention_mask,head_mask=None)[0]
        batch_size,max_len,feat_dim = sequence_output.shape
        valid_output = torch.zeros(batch_size,max_len,feat_dim,dtype=torch.float32,device = torch.device('cpu'))
        for i in range(batch_size):
            jj = -1
            for j in range(max_len):
                    if valid_ids[i][j].item() == 1:
                        jj += 1
                        valid_output[i][jj] = sequence_output[i][j]
        sequence_output = self.dropout(valid_output)
        logits = self.classifier(sequence_output)

        if labels is not None:
            loss_fct = nn.CrossEntropyLoss(ignore_index=0)
            # Only keep active parts of the loss
            #attention_mask_label = None
            if attention_mask_label is not None:
                active_loss = attention_mask_label.view(-1) == 1
                active_logits = logits.view(-1, self.num_labels)[active_loss]
                active_labels = labels.view(-1)[active_loss]
                loss = loss_fct(active_logits, active_labels)
            else:
                loss = loss_fct(logits.view(-1, self.num_labels), labels.view(-1))
            return loss
        else:
            return logits


class NerProcessor():
    """Processor for the CoNLL-2003 data set."""

    def get_examples(self, articleBody):
        """See base class."""
        return self._create_examples(
            readArticle(articleBody), "test") #----SHORTEN calls readfile

    def _create_examples(self,lines,set_type):
        examples = []
        for i,(sentence,label) in enumerate(lines):
            guid = "%s-%s" % (set_type, i)
            text_a = ' '.join(sentence)
            text_b = None
            label = label
            examples.append(InputExample(guid=guid,text_a=text_a,text_b=text_b,label=label))
        return examples

def convert_examples_to_features(examples, label_list, max_seq_length, tokenizer):
    """Loads a data file into a list of `InputBatch`s."""

    label_map = {label : i for i, label in enumerate(label_list,1)}

    features = []
    for (ex_index,example) in enumerate(examples):
        #print(example.text_b)
        textlist = example.text_a.split(' ')
        #print(textlist)
        labellist = example.label
        #print(labellist)
        tokens = []
        labels = []
        valid = []
        label_mask = []
        
        origWords = []
        
        for i, word in enumerate(textlist):
            #print(word) #unmasked
            origWords.append(word)
            token = tokenizer.tokenize(word)
            tokens.extend(token)
            label_1 = labellist[i]
            for m in range(len(token)):
                if m == 0:
                    labels.append(label_1)
                    valid.append(1)
                    label_mask.append(1)
                else:
                    valid.append(0)
        #print("TOKENS: ",tokens) #masked
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
        input_ids = tokenizer.convert_tokens_to_ids(ntokens) #####################################
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
        features.append(
                InputFeatures(input_ids=input_ids,
                              input_mask=input_mask,
                              segment_ids=segment_ids,
                              label_id=label_ids,
                              valid_ids=valid,
                              label_mask=label_mask,
                              origWords = origWords))
    return features

class InputExample(object):
    def __init__(self, guid, text_a, text_b=None, label=None):
        self.guid = guid
        self.text_a = text_a
        self.text_b = text_b
        self.label = label

class InputFeatures(object):
    def __init__(self, input_ids, input_mask, segment_ids, label_id, valid_ids=None, label_mask=None, origWords=[]):
        self.input_ids = input_ids
        self.input_mask = input_mask
        self.segment_ids = segment_ids
        self.label_id = label_id
        self.valid_ids = valid_ids
        self.label_mask = label_mask
        self.origWords = origWords

def readArticle(articleBody):
#FORMAT FOR FILE: word\nword\n...
    data = []
    sentence = []
    label= []
    for sent in articleBody:  
        splits = sent.split(' ')
        for word in splits:
            sentence.append(word.upper()) #do not include the end line
            label.append("O")
        data.append((sentence,label))
        sentence = []
        label = []

    if len(sentence) >0:
        data.append((sentence,label))
        sentence = []
        label = []
    return data

def readBinary(articleBody):
    processor = NerProcessor() #****************
    device = torch.device("cpu") #******DEVICE**********!!!!!!!!!!

    model = Ner.from_pretrained("./out_base")
    tokenizer = BertTokenizer.from_pretrained("./out_base") #do lowercase??

    model.to(device)

    label_list = ["O", "B-chem", "I-chem", "B-quant", "I-quant", "[CLS]", "[SEP]"]

    eval_examples = processor.get_examples(articleBody)
    eval_features = convert_examples_to_features(eval_examples, label_list, 128, tokenizer)

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

    chemicals = []
    quantities = []
    for i in range(len(y_pred)):
        phrase = ""
        for j in range(len(y_pred[i])):
            if('chem' in y_pred[i][j]): #and y_pred[i][j]==y_true[i][j]
                #chemicals.append(words[i][j])
                if j!=(len(y_pred[i])-1) and 'I-' in y_pred[i][j+1]:
                    phrase=phrase+words[i][j]+" "
                elif j==(len(y_pred[i])-1) or "I-" in y_pred[i][j]:
                    if j!=(len(y_pred[i])-1) and "I-" in y_pred[i][j+1]:
                        phrase=phrase+words[i][j]+" "
                    else:
                        phrase=phrase+words[i][j]
                        chemicals.append(phrase)
                        phrase = ""
                elif j==(len(y_pred[i])-1) or 'B-' in y_pred[i][j+1] or 'O' in y_pred[i][j+1]:
                    phrase=phrase+words[i][j]
                    chemicals.append(phrase)
                    phrase = ""
            elif 'quant' in y_pred[i][j]:
                #quantities.append(words[i][j])
                if j!=(len(y_pred[i])-1) and 'I-' in y_pred[i][j+1]:
                    phrase=phrase+words[i][j]+" "
                elif j==(len(y_pred[i])-1) or "I-" in y_pred[i][j]:
                    if j!=(len(y_pred[i])-1) and "I-" in y_pred[i][j+1]:
                        phrase=phrase+words[i][j]+" "
                    else:
                        phrase=phrase+words[i][j]
                        quantities.append(phrase)
                        phrase = ""
                elif j==(len(y_pred[i])-1) or 'B-' in y_pred[i][j+1] or 'O' in y_pred[i][j+1]:
                    phrase=phrase+words[i][j]
                    quantities.append(phrase)
                    phrase = ""

    bad_chars = [',', '”', ',', '"', "'", ")", "("]
    for chem in chemicals:
        for c in bad_chars:
            if c in chem:
                try:
                    chemicals.remove(chem)
                except:
                    chemicals.append(chem.replace(c, ''))
                chemicals.append(chem.replace(c, ''))
    for quant in quantities:
        for c in bad_chars:
            if c in quant:
                try:
                    quantities.remove(quant)
                except:
                    quantities.append(quant.replace(c, ''))
                quantities.append(quant.replace(c, ''))

    chemicals = list(set(chemicals))
    quantities = list(set(quantities))


    return chemicals, quantities
    





                            
