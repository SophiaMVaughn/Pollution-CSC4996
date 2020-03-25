import database
import newspaper
from newspaper import urls as urlChecker
from textColors import bcolors
import json
import sys
from scraper import Scraper
import datetime
from website import Website
from exceptions import WebsiteFailedToInitialize, NextPageException


class Crawler:
    def __init__(self, url, keywords=None, searchPageLimit=2):
        self.baseUrl = url
        self.keywords = keywords
        self.searchPagesArticleLinks = []
        self.recentArticleLinks = []
        self.articleCount = 0
        self.searchPageLimit = searchPageLimit

        # TODO: Consider adding custom exception for this
        self.website = Website(url)


        # TODO: make sure openning websites.json
        with open('websitesTesting.json') as data_file:
            self.websites = json.load(data_file)
            data_file.close()

        for website, attributes in self.websites.items():
            if website in self.baseUrl:
                self.searchQuery = attributes["searchQuery"]
                self.nextPageType = attributes["nextPage"]

        self.exceptions = [
            "https://www.ourmidland.com/",
            "https://www.lakecountystar.com/",
            "https://www.northernexpress.com/",
            "https://www.manisteenews.com/"
        ]

        print("\r" + bcolors.OKGREEN + "[+]" + bcolors.ENDC + " Crawling " +
              self.baseUrl + "..." + bcolors.ENDC, end="")
        sys.stdout.flush()

        self.crawl()

    def crawl(self):
        self.crawlViaSearchKeys()

    def crawlViaSearchKeys(self):

        # TODO: come back to this
        assert self.keywords is not None

        for keyword in self.keywords:

            self.website.searchForKey(keyword)

            links = []
            while self.website.getCurrentPageNum() <= self.searchPageLimit:

                links = self.getPageLinks()

                # TODO: Consider adding custom exception for this
                try:
                    self.website.nextPage()
                except NextPageException:
                    errorLog = open("errorLog.txt", "a+")
                    errorLog.write("Failed to query next page for:   " + self.baseUrl + "\n")
                    errorLog.close()

            if self.baseUrl in self.exceptions:
                articleLinks = self.exceptionFilterLinksForArticles(links)
            else:
                articleLinks = self.filterLinksForArticles(links)

            self.searchPagesArticleLinks = self.searchPagesArticleLinks + articleLinks

        self.articleCount = self.articleCount + len(self.searchPagesArticleLinks)
        self.storeInUrlsCollection(self.searchPagesArticleLinks)

        print("\r" + bcolors.OKGREEN + "[+]" + bcolors.ENDC + " Crawled " + self.baseUrl
              + ": " + bcolors.OKGREEN + str(len(self.searchPagesArticleLinks)) + " URLs retrieved" + bcolors.ENDC)

    def getPageLinks(self):
        page = self.website.getCurrentPage()
        pageLinks = page.find_all('a', href=True)

        links = []

        # TODO: make sure this if statement does what it should to.  If the site uses infinite
        #  scrolling, it will not add links to links list until it's at the last scroll
        if self.nextPageType != 3 or self.website.getCurrentPage() == self.searchPageLimit:
            for link in pageLinks:
                link = link['href']
                if link not in links:
                    links.append(link)

        return links

    # TODO: dead code
    def articlesAreWithinLastYear(self, articleLinks):

        yearAgo = datetime.datetime.now() - datetime.timedelta(days=365)

        for article in articleLinks:
            scraper = Scraper(article)
            scrapedArticle = scraper.getScrapedArticle()

            # TODO: fix this implementation
            if scrapedArticle['publishingDate'] == "":
                continue

            publishingDate = datetime.datetime.strptime(scrapedArticle['publishingDate'], "%m/%d/%Y")
            if publishingDate < yearAgo:
                return False

        return True

    def getRecentArticles(self):
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