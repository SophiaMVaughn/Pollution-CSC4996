import en_core_web_sm
from spacy.matcher import Matcher

nlp = en_core_web_sm.load() #load in the pretrained model from spacy

pPt = Matcher(nlp.vocab) #create a matcher that we can add patterns to

#---------------------------create and declare array of POSITIVE patterns------------
#these are the patterns that chould be found in an event

pollPats = []
#ex: "... dumped into the Detroit River ..."
pollPats.append([{"LEMMA": {
    "IN": ["pollute", "contaminate", "dump", "pour", "discard", "spill", "leak", "taint", "bleed", "plume"]}},
                 {"POS": "ADP", "OP": "?"}, {"POS": "DET", "OP": "?"}, {"POS": "ADP", "OP": "?"}, {"POS": "PROPN"}])
#ex: "...leaked into the drain..."
pollPats.append([{"LEMMA": {
    "IN": ["pollute", "contaminate", "dump", "pour", "discard", "spill", "leak", "taint", "bleed", "plume"]}},
                 {"POS": "ADP", "OP": "?"}, {"POS": "DET", "OP": "?"}, {"POS": "ADP", "OP": "?"}, {"POS": "NOUN"}])
#ex: 
pollPats.append([{"LEMMA": {"IN": ["cause", "source"]}}, {"LEMMA": {
    "IN": ["unknown", "pollute", "contaminate", "dump", "pour", "discard", "spill", "leak", "taint", "bleed",
           "plume"]}}])
pollPats.append([{"POS": "NOUN", "OP": "?"}, {"LEMMA": {"IN": ["superfund"]}}, {"POS": "NOUN", "OP": "?"}])
pollPats.append([{"POS": "NOUN"}, {"LEMMA": {"IN": ["levels", "contamination"]}}])
pollPats.append([{"POS": "NOUN"}, {"LEMMA": {
    "IN": ["pollute", "contaminate", "dump", "pour", "discard", "spill", "leak", "taint", "bleed", "plume"]}}])
pollPats.append([{"LEMMA": {"IN": ["detected", "discovered", "found"]}}, {"POS": "ADJ", "OP": "*"},
                 {"LEMMA": {"IN": ["substance", "chemical", "level"]}}, {"POS": "NOUN", "OP": "?"}])
pollPats.append([{"POS": "ADJ"}, {"LEMMA": {"IN": ["chemical"]}}, {"POS": "NOUN", "OP": "?"}])
pollPats.append([{"POS": "ADJ", "OP": "?"}, {"LEMMA": {"IN": ["chemical"]}}, {"POS": "NOUN"}])
pollPats.append([{"POS": "NUM"}, {"LEMMA": {"IN": ["gallon", "ppt", "ppb", "ton"]}}])
#--------------------------------------------------------------------------------


negP = Matcher(nlp.vocab) #create a second matcher that we can add patterns to
#---------------------------create and declare array of NEGATIVE patterns------------
#these are patterns we noticed often led to a false positive

negPats = []
# identifying lawsuit/sue
negPats.append([{"POS": "NOUN", "OP": "?"}, {"LEMMA": {"IN": ["legislation", "lawsuit", "sue", "charge"]}},
                {"POS": "NOUN", "OP": "?"}])
# op verb + automobile, car, vehicle, motor
negPats.append([{"POS": "VERB", "OP": "?"}, {"LEMMA": {"IN": ["noise", "automobile", "car", "vehicle"]}}])
# op noun + automobile, car, vehicle, motor + op verb
negPats.append(
    [{"POS": "NOUN", "OP": "?"}, {"LEMMA": {"IN": ["automobile", "car", "vehicle"]}}, {"POS": "VERB", "OP": "?"}])
# op verb + championship, game, tournament, competition
negPats.append([{"POS": "VERB", "OP": "?"},
                {"LEMMA": {"IN": ["sport", "basketball", "championship", "game", "tournament", "competition"]}}])
# op verb + fruit, meal, produce, meat + op adverb
negPats.append(
    [{"POS": "VERB", "OP": "?"}, {"LEMMA": {"IN": ["recall", "fruit", "meal", "meat"]}}, {"POS": "ADV", "OP": "?"}])
# op noun + fruit, meal, produce, meat + op adverb
negPats.append([{"POS": "NOUN", "OP": "?"}, {"LEMMA": {"IN": ["fruit", "meal", "meat"]}}, {"POS": "ADV", "OP": "?"}])
# op verb + application, password, technology + op verb
negPats.append([{"POS": "VERB", "OP": "?"}, {"LEMMA": {"IN": ["application", "password", "technology"]}},
                {"POS": "VERB", "OP": "?"}])
# op verb + theater, performance, venue + op verb
negPats.append(
    [{"POS": "VERB", "OP": "?"}, {"LEMMA": {"IN": ["theater", "performance", "venue"]}}, {"POS": "VERB", "OP": "?"}])
# op verb + theater, performance, venue + op noun
negPats.append(
    [{"POS": "VERB", "OP": "?"}, {"LEMMA": {"IN": ["theater", "performance", "venue"]}}, {"POS": "NOUN", "OP": "?"}])
#----------------------------------------------------------------------------

#add all positive patterns from the array of patterns to the first matcher
#The iterator ensures a unique name is given to each pattern added
i = 0
for pat in pollPats:
    pPt.add("pat" + str(i), None, pat)
    i = i + 1

#add all negative patterns from the array of patterns to the second matcher
#The iterator ensures a unique name is given to each pattern added
i = 0
for pat in negPats:
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

def isArticleEvent(article):
    body = article['body']
    tS = convertScrapedtoSent(body)
    numPos = 0
    numNeg = 0
    for sentence in tS:
        #print(sentence)
        nER = nlp(sentence)
        negInSent = negP(nER)
        matchesInSent = pPt(nER)
        if negInSent:
            for mID, s, e in negInSent:
                strID = nlp.vocab.strings[mID]  # convert from span object to string
                startToEnd = nER[s:e]
                numNeg = numNeg + 1
        elif matchesInSent:
            for mID, s, e in matchesInSent:
                strID = nlp.vocab.strings[mID]  # convert from span object to string
                startToEnd = nER[s:e]
                numPos = numPos + 1
    if numPos != 0 and numPos >= numNeg:
        return True
    else:
        return False
    # run at least 2 rules on it
    # returns if it was found to be T/F
