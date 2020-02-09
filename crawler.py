import requests
from bs4 import BeautifulSoup as soup


################################################
#               NewsWebsite Class              #
################################################

class NewsWebsite:
    def __init__(self, url, title, body, publishingDate, nextPage, articles, infinite):
        self.url = url
        self.titleTag = title
        self.bodyTag = body
        self.publishingDateTag = publishingDate
        self.nextPageTag = nextPage
        self.articlesTag = articles
        self.infiniteScrolling = infinite

    def getURL(self):
        return self.url

    def getTitleTag(self):
        return self.titleTag

    def getBodyTag(self):
        return self.bodyTag

    def getPublishingDateTag(self):
        return self.publishingDateTag

    def getNextPageTag(self):
        return self.nextPageTag

    def getArticlesTag(self):
        return self.articlesTag

    def getInfiniteScrolling(self):
        return self.infiniteScrolling

    def getSearchSyntax(self, keyword):
        if "lenconnect" in self.url:
            return "/search?text="+keyword+"&start=1"
        elif "stignacenews" in self.url:
            return "/?s="+keyword

    def getWebsiteName(self):
        websiteName = self.url.split("www.")[1].split(".com")[0]
        return websiteName


################################################
#                Crawler Class                 #
################################################

class Crawler:
    def __init__(self, websiteObj, *keywords):

        # all the list of NewsWebsite objects
        self.website = websiteObj

        # all the article urls crawled by the crawler
        self.urlsCrawled = []

        # all new website urls
        self.baseURLs = []

        # all search keywords
        self.keywords = []

        for key in keywords:
            self.keywords.append(key)

        self.crawl()


    def crawl(self):

        print("\n[+] Crawling...\n")

        for keyword in self.keywords:
            print("[+] Crawling for keyword \'%s\'...\n" % keyword)
            searchURL = self.website.getURL() + self.website.getSearchSyntax(keyword)
            page = requests.get(searchURL)
            soupPage = soup(page.content, 'html.parser')

            # TODO get urls from search page of website

            links = soupPage.find_all(class_=self.website.getArticlesTag())

            # TODO find way to retrieve article urls from search page for the first several news websites
            #  because all we get back is a hash tag, not the url

            for link in links:
                print(link.get_text())
