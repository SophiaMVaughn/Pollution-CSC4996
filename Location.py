
import re
from officialComm import convertScrapedtoSent

def locationsInfo(articleBody):
   # reading from a body of text to find locations
   #test = open("LocationTest.txt", "r")
   lakes = re.compile(r'\S*Lake\S*(?:\s([A-Z]+))\S*')
   rivers = re.compile(r'(?:\S+\s)?\S*River')
   schools = re.compile(r'\S*Elementary School|Intermediate School|Middle School|High School')
   highways = re.compile(r'I-(?:\S+\s)?|M-(?:\S+\s)?')
   cityLoc = re.compile(r'^[A-Z]\w*')
   cities=[]
   cityFile=open("cities.txt","r")
   for x in cityFile:
       cities.append(x.rstrip())
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

  #cities calculation (ONly returns the first city found for right now)
   cities = []
   cityFile = open("Cities.txt", "r")
   for x in cityFile:
       cities.append(x.rstrip())
   city = re.findall(r'[A-Z][a-z]*', articleBody)
   city_set = set(cities)
   for City in city:
       if City in city_set:
           local.append(City)
           break
   return local

