import re
from officialComm import convertScrapedtoSent

def locationsInfo(articleBody):
    # reading from a body of text to find locations
    test = open("LocationTest.txt", "r")
    lakes = re.compile(r'(?i) lake (\w+)')
    rivers = re.compile(r'(?i)\w+(?=\s+river)')
    #store all locations in array
    local = []
    # return all locations found in body of text from file
    for para in articleBody:
        temp= convertScrapedtoSent(para)
        for sent in temp:
            lake=lakes.finall(sent)
            for Lake in lake:
                local.append(Lake)
            river =rivers.findall(sent)
            for River in river:
                local.append(Lake)
    return local