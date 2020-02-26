import newsWebsiteObjs
from crawler import Crawler
from scraper import Scraper
from parse import isArticleEvent
from RNNBinary import readBinary
from officialComm import officialComment
from textColors import bcolors
import testCollectionIncidents
import mainHelper
import database
import sys


####################  create NewsWebsite objects  ###########################
newsWebsiteObjList = newsWebsiteObjs.getNewsWebsiteObjsListForTesting()


####################  crate Crawler objects ###########################
print("\n")
crawlList = []
articleCount = 0
for website in newsWebsiteObjList:
    crawler = Crawler(website, "spills", "dumps")
    articleCount = articleCount + crawler.getArticleCount()
    crawlList.append(crawler)

print("\n" + bcolors.OKGREEN + "[+] " + str(articleCount) + " articles retrieved" + bcolors.ENDC)


####################  create Scraper objects  ###########################
articles = []
articleTitles = []
print("\n")
for website in crawlList:
    for url in website.getCrawledURLs():
        print("\r" + bcolors.OKGREEN + "[+]" + bcolors.ENDC + " Scraping " + url, end="")
        sys.stdout.flush()
        scraper = Scraper(url, newsWebsiteObjList)
        if scraper.getArticleTitle() not in articleTitles:
            articleTitles.append(scraper.getArticleTitle())
            articles.append(scraper)

print("\r" + bcolors.OKGREEN + "[+] All articles scraped" + bcolors.ENDC)


####################  NLP event recognition  ###########################
confirmedEventArticles = []
confirmedEventCount = 0
print("\nParsing event articles")
print("-----------------------")
for article in articles:
    if isArticleEvent(article):
        article.storeInDatabase()
        confirmedEventArticles.append(article)
        confirmedEventCount = confirmedEventCount + 1
        print(bcolors.OKGREEN + "[+] " + article.getArticleTitle() + bcolors.ENDC)
    else:
        print(bcolors.FAIL + "[-] " + article.getArticleTitle() + bcolors.ENDC)

print(bcolors.OKGREEN + "\n[+] " + str(confirmedEventCount) + " event articles found" + bcolors.ENDC)

print("\nConfirmed event articles")
print("-------------------------")
for article in confirmedEventArticles:
    print(bcolors.OKGREEN + "[+] " + article.getArticleTitle() + bcolors.ENDC)


    # #NOTE: ONLY RUN THESE IF YOU HAVE THE out_base FILE WITH THE CORRECT BINARY IN THE DIRECTORY!!!_____________
    # chems, quants = readBinary(article.getArticleBody())
    #
    # if len(chems)>0:
    #     print("CHEMICALS")
    # for chem in chems:
    #     print(chem)
    # if len(quants)>0:
    #     print("QUANTITIES")
    # for quant in quants:
    #     print(quant)


    offComm, people = officialComment(article.getArticleBody())
    # if len(offComm)>0:
    #     print("OFFICIAL COMMENTS")
    #for sent in offComm:
    database.Incidents(
            chemicals=["chem1", "chem2"],
            date="date",
            location="location",
            officialStatement=offComm,
            articleLinks=["www.test.com"]
        ).save()
    if len(people)>0:
        print("PEOPLE")
    for ppl in people:
        print(ppl)
