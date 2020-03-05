import requests
from bs4 import BeautifulSoup as soup
import database
import newspaper
from newspaper import urls as urlChecker
from textColors import bcolors
from demoScript import getUrls
import json

class Crawler:
    def __init__(self, url, keywords=None):
        self.baseUrl = url
        self.keywords = keywords
        self.searchPagesArticleLinks = []
        self.recentArticleLinks = []
        self.articleCount = 0

        with open('websites.json') as data_file:
            self.websites = json.load(data_file)

        for website, attributes in self.websites.items():
            if website in self.baseUrl:
                self.searchQuery = attributes["searchQuery"]

        self.exceptions = [
            "https://www.ourmidland.com/",
            "https://www.lakecountystar.com/",
            "https://www.northernexpress.com/",
            "https://www.manisteenews.com/"
        ]

        self.crawl()

    def crawl(self):
        self.crawlSearchPages()

    def crawlSearchPages(self):

        links = []
        assert self.keywords is not None

        for keyword in self.keywords:
            query = self.searchQuery.replace("PEATKEY", keyword).replace("PEATPAGE", "1")

            page = requests.get(query)

            soupLinks = self.scrapeLinks(page)

            for link in soupLinks:
                if link['href'] not in links:
                    links.append(link['href'])

        if self.baseUrl in self.exceptions:
            self.searchPagesArticleLinks = self.exceptionFilterLinksForArticles(links)
        else:
            self.searchPagesArticleLinks = self.filterLinksForArticles(links)
        self.articleCount = self.articleCount + len(self.searchPagesArticleLinks)
        self.storeInUrlsCollection(self.searchPagesArticleLinks)

        print("\r" + bcolors.OKGREEN + "[+]" + bcolors.ENDC + " Crawling " + self.baseUrl
              + ": " + bcolors.OKGREEN + str(len(self.searchPagesArticleLinks)) + " URLs retrieved" + bcolors.ENDC)

    def crawlRecentArticles(self):
        links = newspaper.build(self.baseUrl, memoize_articles=False)
        for article in links.articles:
            self.recentArticleLinks.append(article.url)
        self.storeInUrlsCollection(self.recentArticleLinks)

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

    def exceptionFilterLinksForArticles(self, links):
        filteredLinks = []

        if self.baseUrl == "https://www.ourmidland.com/":
            for link in links:
                if "/article/" in link:
                    link = "https://www.ourmidland.com" + link
                    filteredLinks.append(link)

        elif self.baseUrl == "https://www.lakecountystar.com/":
            for link in links:
                if "/article/" in link:
                    link = "https://www.lakecountystar.com" + link
                    filteredLinks.append(link)

        elif self.baseUrl == "https://www.northernexpress.com/":
            for link in links:
                if "/news/" in link:
                    linkSplit = link.split("/")
                    if len(linkSplit) > 4:
                        link = "https://www.northernexpress.com" + link
                        filteredLinks.append(link)

        elif self.baseUrl == "https://www.manisteenews.com/":
            for link in links:
                if "/article/" in link:
                    link = "https://www.manisteenews.com" + link
                    filteredLinks.append(link)

        return filteredLinks

    def setBaseUrl(self, url):
        self.baseUrl = url

    def setKeywords(self, keywords):
        self.keywords = keywords

    def getKeywords(self):
        return self.keywords

    def setSearchQueryStructure(self, query):
        self.searchQuery = query

    def scrapeLinks(self, page):
        soupPage = soup(page.content, "html.parser")
        return soupPage.find_all('a', href=True)

    def getArticleLinks(self):
        return self.searchPagesArticleLinks

    def getRecentArticleLinks(self):
        return self.recentArticleLinks

    def getArticleCount(self):
        return self.articleCount

    def storeInUrlsCollection(self, urls):
        for url in urls:
            try:
                database.Urls(url=url).save()
            except:
                pass