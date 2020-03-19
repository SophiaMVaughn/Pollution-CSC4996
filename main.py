from scraperInterface import ScraperInterface
from parse import isArticleEvent
from parse import convertScrapedtoSent
from RNNBinary import readBinary
from officialComm import officialComment
from dateRegex import dateInfo
from textColors import bcolors
from Location import locationsInfo
import testCollectionIncidents
from mongoengine import connect
from dateutil import parser
import database


db = connect(db="Pollution")
db.drop_database("Pollution")

errorLog = open("errorLog.txt","r+")
errorLog.truncate(0)
errorLog.close()

articleBodies = open("articleBodies.txt","r+")
articleBodies.truncate(0)
articleBodies.close()

keywords = ["pollution"]
scraper = ScraperInterface(keywords)

print("\n" + bcolors.OKGREEN + "[+] " + str(scraper.getArticleCount()) + " articles retrieved" + bcolors.ENDC)

articleTitles = []

for article in scraper.getScrapedArticles():
    articleTitles.append(article['title'])

####################  NLP event recognition  ###########################

confirmedEventArticles = []
confirmedEventCount = 0
count = 0
print("\nParsing event articles")
print("-----------------------")

for article in scraper.getScrapedArticles():
    count = count + 1
    if isArticleEvent(article):
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
count = 0
for article in confirmedEventArticles:
    count = count + 1
    print("\n" + bcolors.OKGREEN + "[+] (" + str(count) + "/" + str(len(confirmedEventArticles)) + ") "
          + article['title'] + bcolors.ENDC)
    print(article['url'])

    body = convertScrapedtoSent(article['body'])

    # NOTE: ONLY RUN THESE IF YOU HAVE THE out_base FILE WITH THE CORRECT BINARY IN THE DIRECTORY!!!_____________
    chems, quants = readBinary(body)

    # For getting location information
    locations = locationsInfo(article['body'])

    # for getting official statement
    offComm, people = officialComment(body)

    # for pulling date information
    dates = dateInfo(body)



    if len(dates) == 0:
        date = article['publishingDate']
    else:
        date = dates[0]

    try:
        d = parser.parse(date)
        date = d.strftime("%m/%d/%Y")
    except:
        date = article['publishingDate']

    if len(offComm) is None:
        offComm = ""

    articleLinks = []
    articleLinks.append(article['url'])
    error = False
    if len(locations) == 0:
        location = ""
        error=True
        database.Errors(
                chems=chems,
                day=date,
                loc=location,
                offStmt=offComm,
                artLinks=articleLinks,
                errorMessage="No location found."
            ).save()
        print("Passed-no location")
    else:
        location = locations[0]

    if  len(chems)==0:
        error=True
        database.Errors(
                chems=chems,
                day=date,
                loc=location,
                offStmt=offComm,
                artLinks=articleLinks,
                errorMessage="No chemical found."
            ).save()
        print("Passed-no chemical")

    if error==False:
        scraper.storeInIncidentsCollection(chems, date, location, offComm, articleLinks)

