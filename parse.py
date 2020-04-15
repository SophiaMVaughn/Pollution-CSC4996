import en_core_web_sm
from spacy.matcher import Matcher

nlp = en_core_web_sm.load() #load in the pretrained model from spacy

pollutionPatn = Matcher(nlp.vocab) #create a matcher that we can add patterns to

#---------------------------create and declare array of POSITIVE patterns------------
#these are the patterns that chould be found in an event

pollutionPatterns = []
#ex: "... dumped into the Detroit River ..."
pollutionPatterns.append([{"LEMMA": {
    "IN": ["pollute", "contaminate", "dump", "pour", "discard", "spill", "leak", "taint", "bleed", "plume"]}},
                 {"POS": "ADP", "OP": "?"}, {"POS": "DET", "OP": "?"}, {"POS": "ADP", "OP": "?"}, {"POS": "PROPN"}])
#ex: "...leaked into the drain..."
pollutionPatterns.append([{"LEMMA": {
    "IN": ["pollute", "contaminate", "dump", "pour", "discard", "spill", "leak", "taint", "bleed", "plume"]}},
                 {"POS": "ADP", "OP": "?"}, {"POS": "DET", "OP": "?"}, {"POS": "ADP", "OP": "?"}, {"POS": "NOUN"}])
#ex: "...caused contamination..."
pollutionPatterns.append([{"LEMMA": {"IN": ["cause", "source"]}}, {"LEMMA": {
    "IN": ["unknown", "pollute", "contaminate", "dump", "pour", "discard", "spill", "leak", "taint", "bleed",
           "plume"]}}])
#ex: "... superfund site..."
pollutionPatterns.append([{"POS": "NOUN", "OP": "?"}, {"LEMMA": {"IN": ["superfund"]}}, {"POS": "NOUN", "OP": "?"}])
#ex: "... mercury levels..."
pollutionPatterns.append([{"POS": "NOUN"}, {"LEMMA": {"IN": ["levels", "contamination"]}}])
#ex: "... lead leaked..."
pollutionPatterns.append([{"POS": "NOUN"}, {"LEMMA": {
    "IN": ["pollute", "contaminate", "dump", "pour", "discard", "spill", "leak", "taint", "bleed", "plume"]}}])
#ex: "... found hazardous chemical levels..."
pollutionPatterns.append([{"LEMMA": {"IN": ["detected", "discovered", "found"]}}, {"POS": "ADJ", "OP": "*"},
                 {"LEMMA": {"IN": ["substance", "chemical", "level"]}}, {"POS": "NOUN", "OP": "?"}])
#ex: "... dangerous chemicals..."
pollutionPatterns.append([{"POS": "ADJ"}, {"LEMMA": {"IN": ["chemical"]}}, {"POS": "NOUN", "OP": "?"}])
#ex: "... chemical contamination..."
pollutionPatterns.append([{"POS": "ADJ", "OP": "?"}, {"LEMMA": {"IN": ["chemical"]}}, {"POS": "NOUN"}])
#ex: "... 50,000 gallons..."
pollutionPatterns.append([{"POS": "NUM"}, {"LEMMA": {"IN": ["gallon", "ppt", "ppb", "ton"]}}])
#--------------------------------------------------------------------------------


negativePatn = Matcher(nlp.vocab) #create a second matcher that we can add patterns to
#---------------------------create and declare array of NEGATIVE patterns------------
#these are patterns we noticed often led to a false positive

negativePatterns = []
# identifying lawsuit/sue
negativePatterns.append([{"POS": "NOUN", "OP": "?"}, {"LEMMA": {"IN": ["legislation", "lawsuit", "sue", "charge"]}},
                {"POS": "NOUN", "OP": "?"}])
# op verb + automobile, car, vehicle, motor
negativePatterns.append([{"POS": "VERB", "OP": "?"}, {"LEMMA": {"IN": ["noise", "automobile", "car", "vehicle"]}}])
# op noun + automobile, car, vehicle, motor + op verb
negativePatterns.append(
    [{"POS": "NOUN", "OP": "?"}, {"LEMMA": {"IN": ["automobile", "car", "vehicle"]}}, {"POS": "VERB", "OP": "?"}])
# op verb + championship, game, tournament, competition
negativePatterns.append([{"POS": "VERB", "OP": "?"},
                {"LEMMA": {"IN": ["sport", "basketball", "championship", "game", "tournament", "competition"]}}])
# op verb + fruit, meal, produce, meat + op adverb
negativePatterns.append(
    [{"POS": "VERB", "OP": "?"}, {"LEMMA": {"IN": ["recall", "fruit", "meal", "meat"]}}, {"POS": "ADV", "OP": "?"}])
# op noun + fruit, meal, produce, meat + op adverb
negativePatterns.append([{"POS": "NOUN", "OP": "?"}, {"LEMMA": {"IN": ["fruit", "meal", "meat"]}}, {"POS": "ADV", "OP": "?"}])
# op verb + application, password, technology + op verb
negativePatterns.append([{"POS": "VERB", "OP": "?"}, {"LEMMA": {"IN": ["application", "password", "technology"]}},
                {"POS": "VERB", "OP": "?"}])
# op verb + theater, performance, venue + op verb
negativePatterns.append(
    [{"POS": "VERB", "OP": "?"}, {"LEMMA": {"IN": ["theater", "performance", "venue"]}}, {"POS": "VERB", "OP": "?"}])
# op verb + theater, performance, venue + op noun
negativePatterns.append(
    [{"POS": "VERB", "OP": "?"}, {"LEMMA": {"IN": ["theater", "performance", "venue"]}}, {"POS": "NOUN", "OP": "?"}])
#----------------------------------------------------------------------------

#add all positive patterns from the array of patterns to the first matcher
#The iterator ensures a unique name is given to each pattern added
i = 0
for pat in pollutionPatterns:
    pPt.add("pat" + str(i), None, pat)
    i = i + 1

#add all negative patterns from the array of patterns to the second matcher
#The iterator ensures a unique name is given to each pattern added
i = 0
for pat in negativePatterns:
    negP.add("neg" + str(i), None, pat)
    i = i + 1


#--------function that takes a paragraph and converts it into full sentences-------
def convertScrapedtoSent(splitContent):
    tokenizedSent = []
    NLPtxt = nlp(splitContent) #run the pretrained model on the paragraph
        #NLPtxt contains an attribute called sents that holds full sentences
    for eachSent in NLPtxt.sents: #for each full sentence
        tokenizedSent.append(eachSent.string.strip()) #strip the sentence and add it to the set of sentences
    return tokenizedSent #returns the array of full sentences
#---------------------------------------------------------------------------------

#--------function that takes article and returns if it is or is not an event------
def isArticleEvent(article):
    body = article['body'] #isolate the article body
    tS = convertScrapedtoSent(body) #convert article body to sentences
    numPositivePatterns = 0
    numNegativePatterns = 0
    for sentence in tS: #for each sentence in the article
        nER = nlp(sentence) #convert sentence to NLP object
        negativeInSent = negativePatn(nER) #find all negative patterns in the sentence
        positiveInSent = pollutionPatn(nER) #find all positive patterns in the sentence
        if negativeInSent:
            for mID, s, e in negativeInSent:
                numNegativePatterns = numNegativePatterns + 1 #tally up all of the negative patterns found
        elif positiveInSent:
            for mID, s, e in positiveInSent:
                numPositivePatterns = numPositivePatterns + 1 #tally up all of the positive patterns found

    if numPos != 0 and numPos >= numNeg:
        return True #is an event
    else:
        return False #is not an event
#---------------------------------------------------------------------------------
