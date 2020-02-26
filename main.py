import newsWebsiteObjs
from crawler import Crawler
from scraper import Scraper
from parse import isArticleEvent
from textColors import bcolors
import testCollectionIncidents
import sys


testCollectionIncidents.populateDatabase()

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
print("\n")
for website in crawlList:
    for url in website.getCrawledURLs():
        print("\r" + bcolors.OKGREEN + "[+]" + bcolors.ENDC + " Scraping " + url, end="")
        sys.stdout.flush()
        scraper = Scraper(url, newsWebsiteObjList)
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

