
import re
from officialComm import convertScrapedtoSent

def locationsInfo(articleBody):
   # reading from a body of text to find locations
   #test = open("LocationTest.txt", "r")
   lakes = re.compile(r'\S*Lake\S*(?:\s([A-Z]+))\S*')
   rivers = re.compile(r'(?:\S+\s)?\S*River')
   schools = re.compile(r'(?i)\S*elementary school|intermediate school|middle school|high school')
   highways = re.compile(r'(?i) I-(?:\S+\s)?|M-(?:\S+\s)?')

   #store all locations in array
   local = []
   # return all locations found in body of text from file
   for para in articleBody:
       temp= convertScrapedtoSent(para)
       for sent in temp:
           lake=lakes.findall(sent)
           for Lake in lake:
               local.append(Lake)
               break
           river =rivers.findall(sent)
           for River in river:
               local.append(River)
               break
           school=schools.findall(sent)
           for School in school:
               local.append(School)
               break
           highway = highways.findall(sent)
           for Highway in highway:
               local.append(Highway)
               break
   return local

