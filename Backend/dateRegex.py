import re
from officialComm import convertScrapedtoSent

#identifying individual date patterns
def dateInfo(articleBody):
    #regex pattern to recognize various date patterns
    #examples of what the below pattern recognizes: "04-04-2004; 04/04/04; 4/04/04; 4/4/05; April 04, 2004; March 24, 2004; April. 24, 2004; April 24 2004; 24 Mar 2004; 24 March 2004; 4 June. 2004; 24 August, 2010; Mar 22nd, 2006; Jul 21st, 2007; Mar 24th, 2004; Jan 2009; Dec 2009; Oct 2014; 6/2004; 12/2004; 2018; 2019"
        
    #Establishes the regular expressions pattern to catch dates that are in or similar to the above formats
    #Starts with optional days, goes to optional months, optional numbers, and optional letters in various orders and repetitions
    regex = re.compile(r'(?:Monday|Mon|Tuesday|Tues|Wednesday|Wed|Thursday|Thu|Friday|Fri|Saturday|Sat|Sunday|Sun)?[\s,.]*(?:January|Jan|February|Feb|March|Mar|April|Apr|May|June|Jun|July|Jul|August|Aug|September|Sept|October|Oct|November|Nov|December|Dec)?[\s,.]*(?:\d{1,2}[-/th|st|nd|rd\s]*)(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)?[a-z\s,.]*(?:\d{1,2}[-/th|st|nd|rd)\s,])?(?:\d{2,4})+')
    dates = []
    #For a particular sentence in a sccraped paragraph, a date is identified
    for para in articleBody:
        temp = convertScrapedtoSent(para)
        for sent in temp:
            datePattern = regex.findall(sent)
            #For a specific date, remove any starting space if there is one
            for date in datePattern:
                if date[0]==' ':
                    date = date[1:]
                #The following condition is to eliminate any numbers like "25,000" being picked up as dates because of the comma
                if ',' in date:
                    s = date.split(',')
                    if s[1][0]==' ':
                        if s[1][1].isdigit():
                            #If a comma has a year following it, this date will be appended to the rest of the collected dates from a body of text
                            dates.append(date)
                        else:
                            #Ignore and continue from the entity if it has a comma but the following word is not numbers (25, or 30 should not be a date)
                            continue
                    elif len(s[0])>1 and s[1][0]!=' ' and s[1][0].isdigit() and s[0][-1].isdigit():
                        #Ignore and continue if there is a comma between 2 numbers (300,000)
                        continue
                elif date.isdigit(): #if it is all numbers and nothing else
                    temp = int(date)
                    #Restrict the date timeframe between these years
                    if temp < 1980 or temp > 2020:
                        continue
                    else:
                        dates.append(date)
                #Condition for dashed dates - check individual portions around the dashes by splitting the entity
                elif "-" in date:
                    day = date.split("-")
                    if(len(day)==3):
                     #Condition to make sure that dashed entity really is a date by checking how many indexes are in the split porition
                        if len(day[0])<3 and len(day[1])<3 and len(day[2])<5:
                            dates.append(date)
                #If an enetity does not have a comma or is just numbers, add to the collection of dates
                else:
                    dates.append(date)
    return dates
