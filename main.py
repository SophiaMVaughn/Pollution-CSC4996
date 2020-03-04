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
import database
import sys
import os.path


db = connect(db="Pollution")
db.drop_database("Pollution")

errorLog = open("errorLog.txt","r+")
errorLog.truncate(0)
errorLog.close()

articleBodies = open("articleBodies.txt","r+")
articleBodies.truncate(0)
articleBodies.close()

keywords = ["spills"]
scraper = ScraperInterface(keywords)

print("\n" + bcolors.OKGREEN + "[+] " + str(scraper.getArticleCount()) + " articles retrieved" + bcolors.ENDC)

articleTitles = []

for article in scraper.getScrapedArticles():
    articleTitles.append(article['title'])


####################  NLP event recognition  ###########################
confirmedEventArticles = []
confirmedEventCount = 0
print("\nParsing event articles")
print("-----------------------")
for article in scraper.getScrapedArticles():
    if isArticleEvent(article):
        scraper.storeInArticlesCollection(article)
        confirmedEventArticles.append(article)
        confirmedEventCount = confirmedEventCount + 1
        print(bcolors.OKGREEN + "[+] " + article['title'] + bcolors.ENDC)
    else:
        print(bcolors.FAIL + "[-] " + article['title'] + bcolors.ENDC)

print(bcolors.OKGREEN + "\n[+] " + str(confirmedEventCount) + " event articles found" + bcolors.ENDC)

print("\nRunning NLP analysis")
print("-------------------------")
i = 0
for article in confirmedEventArticles:
    print(bcolors.OKGREEN + "[+] " + article['title'] + bcolors.ENDC)

    body = convertScrapedtoSent(article['body'])

    # NOTE: ONLY RUN THESE IF YOU HAVE THE out_base FILE WITH THE CORRECT BINARY IN THE DIRECTORY!!!_____________
    chems, quants = readBinary(body)

    # For getting location information
    location = locationsInfo(body)

    offComm, people = officialComment(body)

    # for pulling date information
    dates = dateInfo(body)

    if len(location) == 0:
        location = ["none"]

    if len(dates) == 0:
        dates = ["none"]

    for chem in chems:
        print(chem)

    # scraper.storeInIncidentsCollection(chems, dates[0], location[0], offComm, article['url'])

    database.Incidents(
        chemicals=chems,
        date=dates[0],
        location=location[0],
        officialStatement=offComm,
        articleLinks=[article['url']]
    ).save()
