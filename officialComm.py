#given the body of the article
#use POS tagging to find official statement
#find any date mentioned

#call the RNN binary on the body (what format should it be in?? how to call from script??)

#enter everything into the database

import spacy
import en_core_web_sm
from spacy.matcher import Matcher

nlp = en_core_web_sm.load()
pPt = Matcher(nlp.vocab)
pPt.add("pat1",None,
        [{"POS": "PROPN"},{"POS": "PUNCT", "OP":"?"}, {"POS": "DET", "OP":"?"},{"LEMMA": {"IN": [
                            "director","engineer","governer","mayor","manager",
                           "official","commissioner","representative", "chief", "coordinator"]}}]
        )
pPt.add("pat2",None,
        [{"LEMMA": {"IN": ["announce", "hazard", "say", "stated", "issued", "warned"]}},
        {"POS":"NOUN","OP":"*"},{"LEMMA": {"IN": ["director","engineer","governer","mayor","manager",
                           "official","commissioner","representative","cheif","coordinator"]}}]
        )
pPt.add("pat3",None,[{"LEMMA": {"IN": ["official","Official"]}},
                     {"LEMMA": {"IN": ["announce", "hazard", "say", "stated", "issued","warned"]}}]) #lemmatized words (said/discussed/etc.)

pPt.add("pat4",None,
        [{"LEMMA": {"IN": ["According", "according"]}}])

negP = Matcher(nlp.vocab)
negP.add("pat1",None,
        [{"LEMMA": {"IN": ["foundation", "non-profit", "company","spokesperson",
                           "spokeswoman","spokesman"]}}])
class locatedData:
    def __init__(self):
        chemicals = []
        date = ""
        #official stmt should be tuples (stmt, official title, name [optional])
        officialStmts = []
        quantities = []
        locations = []
        primaryLoc = ""
        #other locations (rivers, addresses, etc)??
        #otherLoc = []
        


def convertScrapedtoSent(splitContent):
    tokenizedSent = []
    #tokenize
    NLPtxt = nlp(splitContent)
    for eachSent in NLPtxt.sents:
        tokenizedSent.append(eachSent.string.strip())
    return tokenizedSent


def officialComment(articleBody):
    results = []
    people = []
    for para in articleBody:
        temp = convertScrapedtoSent(para)
        for sent in temp:
            nER = nlp(sent)        
            matchesInSent = pPt(nER)
            neg1 = negP(nER)
            lowersent = nlp(sent.lower())
            secondMatch = pPt(lowersent)
            neg2 = negP(lowersent)
            if neg1 or neg2:
                continue
            elif matchesInSent or secondMatch:
                
                for entity in nER.ents:
                    if entity.label_=="PERSON":
                        people.append(entity.text)
                results.append(sent)
    return results, people





