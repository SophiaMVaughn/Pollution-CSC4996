from scraperInterface import ScraperInterface
from parse import isArticleEvent
from parse import convertScrapedtoSent
from RNNBinary import readBinary
from officialComm import officialComment
from dateRegex import dateInfo
from textColors import bcolors
from Location import locationsInfo
from mongoengine import connect
from dateutil import parser
from datetime import date

# delete the Pollution database (for testing only)
db = connect(db="Pollution")
db.drop_database("Pollution")

# delete content in error log
errorLog = open("errorLog.txt","r+")
errorLog.truncate(0)
errorLog.close()

# delete text file holding article bodies after scrape
articleBodies = open("articleBodies.txt","r+")
articleBodies.truncate(0)
articleBodies.close()

# delete text file holding crawled websites
crawlLog = open("crawlLog.txt","r+")
crawlLog.truncate(0)
crawlLog.close()

# delete text file holding article urls scraped
scrapeLog = open("scrapeLog.txt", "r+")
scrapeLog.truncate(0)
scrapeLog.close()

####################  Article scraping  ###########################

# set the keywords to use in crawler
keywords = ["pollution", "contamination", "spill"]

# instantiate ScraperInterface object, passing the keywords list, setting a search page limit of 10,
# and setting the json file to pull websites/website attributes from to website.json
scraper = ScraperInterface(keywords, searchPageLimit=10, websitesJsonFile="websites.json")

print("\n" + bcolors.OKGREEN + "[+] " + str(scraper.getArticleCount()) + " articles scraped" + bcolors.ENDC)

# array to hold article titles
articleTitles = []

# loop through list of article dictionary objects, each dictionary holding scraped values of a
# particular article (title, date, body) and append each article title to articleTitles list
for article in scraper.getScrapedArticles():
    articleTitles.append(article['title'])

####################  NLP event recognition  ###########################

# list of articles about contamination events
confirmedEventArticles = []

# counter to track number of contamination event articles
confirmedEventCount = 0

count = 0
print("\nParsing event articles")
print("-----------------------")

# for every article found
for article in scraper.getScrapedArticles():
    count = count + 1

    # if it is determined to be an event
    if isArticleEvent(article):
        # insert article in the Articles collection
        scraper.storeInArticlesCollection(article)

        confirmedEventArticles.append(article)
        confirmedEventCount = confirmedEventCount + 1

        print(bcolors.OKGREEN + "[+] (" + str(count) + "/" + str(len(scraper.getScrapedArticles()))
              + ") " + article['title'] + bcolors.ENDC)
    else:
        print(bcolors.FAIL + "[-] (" + str(count) + "/" + str(len(scraper.getScrapedArticles()))
              + ") " + article['title'] + bcolors.ENDC)

print(bcolors.OKGREEN + "\n[+] " + str(confirmedEventCount) + " event articles found" + bcolors.ENDC)

print("\nRunning NLP analysis")
print("-------------------------")

# open weekly log file to hold events inserted into Incidents collection
count = 0
weeklyRunLogs = open('weeklyRunLogs.txt', 'a+')
# setting and writing the date of the run to the log file
today = date.today()
weeklyRunLogs.write("\n************  " + str(today) + "  ************\n\n")
# write the number of incidents retrieved to the log file
weeklyRunLogs.write("Incidents retrieved: " + str(len(confirmedEventArticles)) + "\n\n")

####################### NLP event attributes extraction ########################

# for each confirmed contamination event article
for article in confirmedEventArticles:
    count = count + 1
    print("\n" + bcolors.OKGREEN + "[+] (" + str(count) + "/" + str(len(confirmedEventArticles)) + ") "
          + article['title'] + bcolors.ENDC)

    # parse the body into paragraphs
    body = convertScrapedtoSent(article['body'])

    # retrieve chemicals from the body
    chems = readBinary(body)

    # For getting location information
    locations = locationsInfo(body)
    
    # for getting official statement
    offComm = officialComment(body)

    # for pulling date information
    dates = dateInfo(body)

    # if no date was found
    if len(dates) == 0:
        # use the publicshiing date of the article
        date = article['publishingDate']
    else:
        date = dates[0]

    try:
        # attempt to format the date
        d = parser.parse(date)
        date = d.strftime("%m/%d/%Y")

    # if it failed, use the publishing date
    except:
        date = article['publishingDate']

    # if there is not an official comment found
    if len(offComm) is None:
        offComm = ""

    articleLinks = []
    articleLinks.append(article['url'])
    error = False

    # remove bad locations
    if len(locations) == 0: # no locations found
        location = ""
    # some locations found
    else:
        # for each location
        for location in locations:
            # if a location is a tuple (bad)
            if(type(location) is tuple):
                # remove the location
                locations.remove(location)
                continue
            # if it is not a tuple
            else:
                # make that the location
                location = locations[0]
                break
    # if the type is a tuple, it contains a good location somewhere in there, so find it and use it
    if type(location) is tuple:
        for t in location:
            if (len(t) > 0):
                location = t
            break
    # final level of error handling
    try:
        print("final location: "+location)
    except:
        location = ""

    # store all attributes of the event (chemicals involved, location, date, official statement, and
    # related article links) into Incidents collection
    scraper.storeInIncidentsCollection(chems, date, location, offComm, articleLinks)

    # insert event ant and it's attributes into the weekly log file
    weeklyRunLogs.write("Event #" + str(count) + " - ")
    weeklyRunLogs.write("Date: " + str(date) + "; ")
    weeklyRunLogs.write("Location: " + str(location) + "; ")
    weeklyRunLogs.write("Chems: " + str(chems) + "; ")
    weeklyRunLogs.write("Article Links: " + str(articleLinks) + "\n")

# close weekly log file
weeklyRunLogs.close()




