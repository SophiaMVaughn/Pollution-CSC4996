import requests
from bs4 import BeautifulSoup as soup


################################################
#               NewsWebsite Class              #
################################################

class NewsWebsite:
    def __init__(self, url, title, body, publishingDate, nextPage, articles, search, infinite):
        self.url = url
        self.titleTag = title
        self.bodyTag = body
        self.publishingDateTag = publishingDate
        self.nextPageTag = nextPage
        self.articlesTag = articles
        self.searchSyntax = search
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

    def getSearchSyntax(self):
        return self.searchSyntax


################################################
#                Crawler Class                 #
################################################

class Crawler:
    def __init__(self, websiteObjs, *keywords):

        # all the list of NewsWebsite objects
        self.websiteObjs = websiteObjs

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

        print("[+] Crawling...\n")

        for website in self.websiteObjs:

            for keyword in self.keywords:

                searchURL = website.getURL() + website.getSearchSyntax() + keyword
                page = requests.get(searchURL)
                soupPage = soup(page.content, 'html.parser')
                links = soupPage.find_all(website.getArticlesTag(), href=True)

                # TODO loop through links and extract the links that are article urls
                #  (maybe add another attribut to NewsWebsite class that specifies what these
                #  links will look like

                for link in links:
                    print(link['href'])


