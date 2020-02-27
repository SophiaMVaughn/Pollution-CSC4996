import requests
from bs4 import BeautifulSoup as soup
from textColors import bcolors
import database


################################################
#                Crawler Class                 #
################################################

class Crawler:
    def __init__(self, websiteObj, *keywords):

        self.website = websiteObj

        # all the article urls crawled by the crawler
        self.urlsCrawled = []

        # all search keywords
        self.keywords = []

        self.articleCount = 0

        for key in keywords:
            self.keywords.append(key)

        self.crawl()
        self.storeInDatabase()

    def crawl(self):

        for keyword in self.keywords:
            # TODO: work on moving through pages
            searchURL = self.website.getSearchQuery(keyword, 1)
            page = requests.get(searchURL)
            soupPage = soup(page.content, 'html.parser')

            links = soupPage.find_all('a', href=True)

            articleCountPerKey = 0

            for link in links:

                link = link['href']

                if self.website.getURL() not in link:
                    link = self.website.getURL() + link

                # TODO: for some websites, different article types have different link structures
                #  but you can search for common structure attribute in the link
                if (self.website.getURL() + self.website.getArticleLinkStructure()) in link:
                    self.urlsCrawled.append(link)
                    self.articleCount = self.articleCount + 1
                    articleCountPerKey = articleCountPerKey + 1

            print(bcolors.OKGREEN + "[+]" + bcolors.ENDC + " Crawling " + self.website.getWebsiteName() +
                  ".com for keyword " + bcolors.WARNING + "\'%s\'" % (keyword) + bcolors.ENDC + ": " +
                  bcolors.OKGREEN + str(articleCountPerKey) + " URLs retrieved" + bcolors.ENDC)

    def storeInDatabase(self):
        for url in self.getCrawledURLs():
            try:
                database.Urls(url=url).save()
            except:
                pass

    def getCrawledURLs(self):
        return self.urlsCrawled

    def getArticleCount(self):
        return self.articleCount
