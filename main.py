from newsWebsite import NewsWebsite
import newsWebsiteObjs
from crawler import Crawler
from scraper import Scraper
from parse import isArticleEvent
from textColors import bcolors


####################  create NewsWebsite objects  ###########################
newsWebsiteObjList = newsWebsiteObjs.getNewsWebsiteObjsListForTesting()

# crate Crawler objects
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
        scraper = Scraper(url, newsWebsiteObjList)
        articles.append(scraper)


####################  NLP event recognition  ###########################
confirmedEventArticles = []
print("\nParsing event articles")
print("-----------------------")
for article in articles:
    if isArticleEvent(article):
        print(bcolors.OKGREEN + "[+] " + article.getArticleTitle() + bcolors.ENDC)
        confirmedEventArticles.append(article)
    else:
        print(bcolors.FAIL + "[-] " + article.getArticleTitle() + bcolors.ENDC)

print("\nConfirmed event articles")
print("-------------------------")
for article in confirmedEventArticles:
    print(bcolors.OKGREEN + "[+] " + article.getArticleTitle() + bcolors.ENDC)

