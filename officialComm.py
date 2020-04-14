import en_core_web_sm
from spacy.matcher import Matcher

nlp = en_core_web_sm.load() #load in the english pretrained spacy model
pPt = Matcher(nlp.vocab) #create a matcher that we can add patterns to

#-------------------------patterns being added to the matcher----------------------------
#pattern to recognize "(name) (optional ,) (optional the) (any lemmatized title)"
pPt.add("pat1",None,
        [{"POS": "PROPN"},{"POS": "PUNCT", "OP":"?"}, {"POS": "DET", "OP":"?"},{"LEMMA": {"IN": [
                            "director","engineer","governer","mayor","manager",
                           "official","CEO","COO","commissioner","spokesperson",
                           "spokeswoman","spokesman","representative", "chief", "coordinator"]}}]
        )
#pattern to recognize "(lemmatized verb) (optional noun) (any lemmatized title)"
pPt.add("pat2",None,
        [{"LEMMA": {"IN": ["announce", "hazard", "say", "stated", "issued", "warned"]}},
        {"POS":"NOUN","OP":"*"},{"LEMMA": {"IN": ["director","engineer","governer","mayor","manager",
                           "official","CEO","COO","commissioner","spokesperson",
                           "spokeswoman","spokesman","representative","cheif","coordinator"]}}]
        )
#pattern to recognize "(lemmatized official) (lemmatized verb)
pPt.add("pat3",None,[{"LEMMA": {"IN": ["official","Official"]}},
                     {"LEMMA": {"IN": ["announce", "hazard", "say", "stated", "issued","warned"]}}])
#pattern to recognize any sentence beginning with "According to..."
pPt.add("pat4",None,
        [{"LEMMA": {"IN": ["According", "according"]}}])

#------------------------------------end of pattern declaration-----------------------#


#--------function that takes a paragraph and converts it into full sentences-------
def convertScrapedtoSent(splitContent):
    tokenizedSent = []
    NLPtxt = nlp(splitContent) #run the pretrained model on the paragraph
        #NLPtxt contains an attribute called sents that holds full sentences
    for eachSent in NLPtxt.sents: #for each full sentence
        tokenizedSent.append(eachSent.string.strip()) #strip the sentence and add it to the set of sentences
    return tokenizedSent #returns the array of full sentences


#------function that takes the article body (array of paragraphs)-----------
#returns an array of sentences that contain official statements
def officialComment(articleBody):
    results = []
    for para in articleBody: #for each paragraph in the article
        temp = convertScrapedtoSent(para) #convert that paragraph to sentences
        for sent in temp: #for each of those sentences
            nER = nlp(sent) #run the nlp model on the sentence
            matchesInSent = pPt(nER) #filter the sentence through the matcher
                #(find all of the matching patterns)
            lowersent = nlp(sent.lower()) #run the nlp model on the lower case sentence
            secondMatch = pPt(lowersent) #filter that sentence through the matcher
                #(find all of the matching patterns)
            if matchesInSent or secondMatch: #if either returned a match
                results.append(sent) #add that sentence as an official comment
    
    return results #return array of all pattern-matching sentences




