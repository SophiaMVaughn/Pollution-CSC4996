from newsWebsite import NewsWebsite
from crawler import Crawler
from scraper import Scraper

# create NewsWebsite objects
newsWebsiteObjList = []

# newsWebsiteObjList.append(NewsWebsite("https://www.stignacenews.com",
#                                       "title", "", "", "https://www.stignacenews.com/page/PEATPAGE/?s=PEATKEY",
#                                       "/articles/", False))

newsWebsiteObjList.append(NewsWebsite("https://www.ourmidland.com", "title", "p", "time",
                                      "https://www.ourmidland.com/search/?action=search&searchindex=solr&query=PEATKEY&page=PEATPAGE",
                                      "/news/article/", False))

newsWebsiteObjList.append(NewsWebsite("https://www.michigansthumb.com/", "title", "p", "time",
                                      "https://www.michigansthumb.com/search/?action=search&searchindex=solr&query=PEATKEY&page=PEATPAGE",
                                      "/news/article", False))

# crate Crawler objects
print("\n")
crawlList = []
for website in newsWebsiteObjList:
    crawlList.append(Crawler(website, "pollution", "contamination"))

# create Scraper objects
print("\n")
for website in crawlList:
    for url in website.getCrawledURLs():
        scraper = Scraper(url, newsWebsiteObjList)