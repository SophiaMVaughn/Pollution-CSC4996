import re
from officialComm import convertScrapedtoSent
def locationsInfo(articleBody):
    # reading from a body of text to find locations

    #All regular expressions which either look at the words before or after the keyword to detect for locations

    #The lakes regular expression looks for words after the word Lake which are capitalized and not numbers
    lakes = re.compile(r'\S*Lake*(?:\s\S*)([A-Z]\S*)')
    # The rivers regular expression looks for words before the word River which are capitalized and not numbers
    rivers = re.compile(r'([A-Z]\S*)(?:\S+\s)?\S*River')
    # The schools regular expression will look for one or two words before every keyword which are both capitalized and not numbers
    schools = re.compile(r'([A-Z]\S*)(?:\S+\s)?\S*Elementary School|([A-Z]\S*)(?:\S+\s)?\S*Intermediate School|([A-Z]\S*)(?:\S+\s)?\S*Middle School|([A-Z]\S*)(?:\S+\s)?\S*High School|([A-Z]\S*)(?:\S+\s)?\S*Public School|([A-Z]\S*)(?:\S+\s)?\S*Private School|([A-Z]\S*)(?:\S+\s)?\S*Academy')
    # The highways regular expression will look for numbers right after the I- and M-
    highways = re.compile(r'I-(?:\S+\s)\s?|M-(?:\S+\s)\s?')
    # The word before will look for words before the keyword which are both capitalized and not numbers
    wordBefore = re.compile(r'([A-Z]\S*)(?:\S+\s)?\S*County|([A-Z]\S*)(?:\S+\s)?\S*Lake|([A-Z]\S*)(?:\S+\s)?\S*Townships|([A-Z]\S*)(?:\S+\s)?\S*Park|([A-Z]\S*)(?:\S+\s)?\S*Bay|([A-Z]\S*)(?:\S+\s)?\S*Pond|([A-Z]\S*)(?:\S+\s)?\S*Dam|([A-Z]\S*)(?:\S+\s)?\S*Delta|([A-Z]\S*)(?:\S+\s)?\S*Creek|([A-Z]\S*)(?:\S+\s)?\S*Power Plant|([A-Z]\S*)(?:\S+\s)?\S*Power Station')
    cities = []
    cityFile = open("Cities.txt", "r")
    for x in cityFile:
        cities.append(x.rstrip())
    # store all locations in array
    local = []
    # return all locations found in body of text from file
    for para in articleBody:
        temp = convertScrapedtoSent(para)
        for sent in temp:
            lake = lakes.findall(sent)
            for Lake in lake:
                local.append(Lake)
                break
            river = rivers.findall(sent)
            for River in river:
                local.append(River)
                break
            school = schools.findall(sent)
            for School in school:
                local.append(School)
                break
            highway = highways.findall(sent)
            for Highway in highway:
                local.append(Highway)
                break
            wordsBefore = wordBefore.findall(sent)
            for wordbefore in wordsBefore:
                local.append(wordbefore)
                break
    # Cities calculation
    cities = []
    cityFile = open("Cities.txt", "r")
    #Sanitizes input from cities text file
    for x in cityFile:
        cities.append(x.rstrip().upper())
    city_set = set(cities)
    #For loop which loops through the words in the article paragraphs
    for para in articleBody:
        temp = convertScrapedtoSent(para)
        for sent in temp:
            city = re.findall(r'[A-Z][a-z]*', sent)
            citypair = ""
            for i in range(len(city)):
                if (i != len(city) - 1):
                    citypair = city[i] + " " + city[i + 1]
                if city[i].upper() in city_set:
                    local.append(city[i])
                elif citypair.upper() in city_set:
                    local.append(citypair)
    cityFile.close()
    #Gets rid of commas
    for l in local:
        if(type(l) is tuple):
            for x in l:
                if len(x)>0:
                    local.append(x)
            local.remove(l)
    return local
