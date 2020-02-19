from newsWebsite import NewsWebsite
from crawler import Crawler
from scraper import Scraper
from parse import isArticleEvent
from textColors import bcolors

# create NewsWebsite objects
newsWebsiteObjList = []

# newsWebsiteObjList.append(NewsWebsite("https://www.stignacenews.com",
#                                       "title", "", "", "https://www.stignacenews.com/page/PEATPAGE/?s=PEATKEY",
#                                       "/articles/", False))

# newsWebsiteObjList.append(NewsWebsite("https://www.ourmidland.com", "title", "p", "time",
#                                       "https://www.ourmidland.com/search/?action=search&searchindex=solr&query=PEATKEY&page=PEATPAGE",
#                                       "/news/article/", False))

newsWebsiteObjList.append(NewsWebsite("https://www.michigansthumb.com/", "title", "p", "time",
                                      "https://www.michigansthumb.com/search/?action=search&searchindex=solr&query=PEATKEY&page=PEATPAGE",
                                      "/news/article", False))

# crate Crawler objects
print("\n")
crawlList = []
articleCount = 0
for website in newsWebsiteObjList:
    crawler = Crawler(website, "pollution", "contamination")
    articleCount = articleCount + crawler.getArticleCount()
    crawlList.append(crawler)

print("\n" + bcolors.OKGREEN + "[+] " + str(articleCount) + " articles retrieved" + bcolors.ENDC)

# create Scraper objects
articles = []
print("\n")
for website in crawlList:
    for url in website.getCrawledURLs():
        scraper = Scraper(url, newsWebsiteObjList)
        articles.append(scraper)

# NLP event recognition
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

