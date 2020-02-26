import re
from officialComm import convertScrapedtoSent

#identifying individual date patterns
def dateInfo(articleBody):
    #regex pattern to recognize various date patterns
    #examples: "04-04-2004; 04/04/04; 4/04/04; 4/4/05; April 04, 2004; March 24, 2004; April. 24, 2004; April 24 2004; 24 Mar 2004; 24 March 2004; 4 June. 2004; 24 August, 2010; Mar 22nd, 2006; Jul 21st, 2007; Mar 24th, 2004; Jan 2009; Dec 2009; Oct 2014; 6/2004; 12/2004; 2018; 2019"
    regex = re.compile(r'(?:January|Jan|February|Feb|March|Mar|April|Apr|May|June|Jun|July|Jul|August|Aug|September|Sept|October|Oct|November|Nov|December|Dec)*[\s,.]*(?:\d{1,2}[-/th|st|nd|rd\s]*)(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)?[a-z\s,.]*(?:\d{1,2}[-/th|st|nd|rd)\s,]*)+(?:\d{2,4})+')
    dates = []
    for para in articleBody:
        temp = convertScrapedtoSent(para)
        for sent in temp:
            datePattern = regex.findall(sent)
            for date in datePattern:
                dates.append(date)
    return dates
