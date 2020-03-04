import requests
from bs4 import BeautifulSoup as soup
import database
import newspaper
from newspaper import urls as urlChecker
from textColors import bcolors


class Crawler:
    def __init__(self):
        self.baseUrl = ""
        self.keywords = []
        self.articleLinks = []
        self.homePageArticleLinks = []
        self.articleCount = 0

    def crawl(self):
        links = []
        for keyword in self.keywords:
            query = self.searchQuery.replace("PEATKEY", keyword).replace("PEATPAGE","1")

            page = requests.get(query)

            soupLinks = self.scrapeArticleLinks(page)

            for link in soupLinks:
                if link['href'] not in links:
                    links.append(link['href'])

        self.articleLinks = self.filterLinksForArticles(links)
        self.articleCount = self.articleCount + len(self.articleLinks)
        self.storeInUrlsCollection(self.articleLinks)

        # print("\r" + bcolors.OKGREEN + "[+]" + bcolors.ENDC + " Crawling " + self.baseUrl
        #       + " for keyword " + bcolors.WARNING + "\'%s\'" % (keyword) + bcolors.ENDC + ": " +
        #       bcolors.OKGREEN + str(len(self.articleLinks)) + " URLs retrieved" + bcolors.ENDC)

        print("\r" + bcolors.OKGREEN + "[+]" + bcolors.ENDC + " Crawling " + self.baseUrl
              + ": " + bcolors.OKGREEN + str(len(self.articleLinks)) + " URLs retrieved" + bcolors.ENDC)

    def crawlHomePage(self):
        links = newspaper.build(self.baseUrl, memoize_articles=False)
        for article in links.articles:
            self.homePageArticleLinks.append(article.url)
        self.storeInUrlsCollection(self.homePageArticleLinks)

    def filterLinksForArticles(self, urls):
        validArticleUrls = []
        for url in urls:
            if "http" not in url:
                url = self.baseUrl + url
            urlSplit = url.split("/")
            if len(urlSplit) < 5:
                continue
            if urlSplit[-2:-1][0].isnumeric() and urlSplit[-3:-2][0].isnumeric():
                continue
            if urlChecker.valid_url(url):
                validArticleUrls.append(url)
        return validArticleUrls

    def setBaseUrl(self, url):
        self.baseUrl = url

    def setKeywords(self, keywords):
        self.keywords = keywords

    def getKeywords(self):
        return self.keywords

    def setSearchQueryStructure(self, query):
        self.searchQuery = query

    def scrapeArticleLinks(self, page):
        # TODO: try overriding this in the website classes and use tree structure of search pages
        #  to get article urls
        soupPage = soup(page.content, "html.parser")
        return soupPage.find_all('a', href=True)

    def getArticleLinks(self):
        return self.articleLinks

    def getArticleCount(self):
        return self.articleCount

    def storeInUrlsCollection(self, urls):
        for url in urls:
            try:
                database.Urls(url=url).save()
            except:
                pass