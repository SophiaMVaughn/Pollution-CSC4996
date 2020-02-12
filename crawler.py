import requests
from bs4 import BeautifulSoup as soup


################################################
#               NewsWebsite Class              #
################################################

class NewsWebsite:
    def __init__(self, articleURL, titleTag, bodyTag, publishingDateTag, nextPageTag, articleLinkStructure, infiniteScrolling):
        self.articleURL = articleURL
        self.titleTag = titleTag
        self.bodyTag = bodyTag
        self.publishingDateTag = publishingDateTag
        self.nextPageTag = nextPageTag
        self.articleLinkStructure = articleLinkStructure
        self.infiniteScrolling = infiniteScrolling

    def getURL(self):
        return self.articleURL

    def getTitleTag(self):
        return self.titleTag

    def getBodyTag(self):
        return self.bodyTag

    def getPublishingDateTag(self):
        return self.publishingDateTag

    def getNextPageTag(self):
        return self.nextPageTag

    def getArticleLinkStructure(self):
        return self.articleLinkStructure

    def getInfiniteScrolling(self):
        return self.infiniteScrolling

    def getSearchQuery(self, keyword, pageNum):
        # TODO: implement
        if "stignacenews" in self.articleURL:
            return "https://www.stignacenews.com/page/" + str(pageNum) + "/?s=" + keyword

    def getWebsiteName(self):
        websiteName = self.articleURL.split("www.")[1].split(".com")[0]
        return websiteName


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

        for key in keywords:
            self.keywords.append(key)

        self.crawl()


    def crawl(self):

        print("\n[+] Crawling...\n")

        for keyword in self.keywords:
            print("[+] Crawling " + self.website.getWebsiteName() + ".com for keyword \'%s\'...\n" % keyword)
            searchURL = self.website.getSearchQuery(keyword, 1)
            page = requests.get(searchURL)
            soupPage = soup(page.content, 'html.parser')

            links = soupPage.find_all('a', href=True)

            for link in links:
                if self.website.getArticleLinkStructure() in link['href']:
                    self.urlsCrawled.append(link['href'])

    def getCrawledURLs(self):
        return self.urlsCrawled

