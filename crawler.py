import database
import newspaper
from newspaper import urls as urlChecker
from textColors import bcolors
import json
import sys
from website import Website
from exceptions import WebsiteFailedToInitialize, NextPageException


# The Crawler class serves to connect to a website and retrieve article urls, both recent and past articles

class Crawler:

    # Constructor for the Crawler class
    def __init__(self, url, keywords=None, searchPageLimit=2, websitesJsonFile="websites.json"):

        # iinitialize class attributes
        self.baseUrl = url
        self.keywords = keywords
        self.articleLinks = []
        self.articleCount = 0
        self.searchPageLimit = searchPageLimit
        self.websitesJsonFile = websitesJsonFile

        # instantiate a Website object to interact with the website to be crawled
        try:
            self.website = Website(url, websitesJsonFile=self.websitesJsonFile)

        # raise exception if there is an error connecting to the website
        except WebsiteFailedToInitialize:
            raise WebsiteFailedToInitialize(url)

        # open the json file containing websites and their attributes
        with open(self.websitesJsonFile) as data_file:
            self.websites = json.load(data_file)
            data_file.close()

        # set the searchQuery attribute to the approapriate search query structure in the websites json file
        for website, attributes in self.websites.items():
            if website in self.baseUrl:
                self.searchQuery = attributes["searchQuery"]

        # populate the exceptions attribute list with websites who's article urls need to be manually
        # crawled
        self.exceptions = [
            "https://www.ourmidland.com/",
            "https://www.lakecountystar.com/",
            "https://www.northernexpress.com/",
            "https://www.manisteenews.com/"
        ]

        print("\r" + bcolors.OKGREEN + "[+]" + bcolors.ENDC + " Crawling " +
              self.baseUrl + "..." + bcolors.ENDC, end="")
        sys.stdout.flush()

        # start crawling
        self.crawl()

        print("\r" + bcolors.OKGREEN + "[+]" + bcolors.ENDC + " Crawled " + self.baseUrl
              + ": " + bcolors.OKGREEN + str(len(self.articleLinks)) + " URLs retrieved" + bcolors.ENDC)

    # For the first crawl, make call to both the crawlViaSearchKeys method and the getRecentArticles method,
    # but for the weekly crawls, comment out the crawlViaSearchKeys method so that only recent articles are
    # retrieved
    def crawl(self):
        self.crawlViaSearchKeys()
        # self.crawlRecentArticles()

    # Crawl the website by making search queries to the website (with the keyword(s) specified in the
    # keywords attribute) using the website's search functionality. The method will visit the first page
    # of the search page result and will continue to the next page as many times as specified by the
    # searchPageLimit attribute
    def crawlViaSearchKeys(self):

        # make sure the keywords attribute is not empty
        assert self.keywords is not None

        for keyword in self.keywords:

            # use the Website attribute searchForKey to set the object's current url as the url of the
            # keyword search query
            self.website.searchForKey(keyword)

            # keep searching next page until the current page number is less than the searchPageLimit
            # attribute
            while self.website.getCurrentPageNum() <= self.searchPageLimit:

                # assign all links found from the current web page of the Website object
                links = self.getPageLinks()

                # filter links in the links variable to get only the article links
                if self.baseUrl in self.exceptions:
                    articleLinks = self.exceptionFilterLinksForArticles(links)
                else:
                    articleLinks = self.filterLinksForArticles(links)

                # populate articleLinks attribute with more links
                self.articleLinks = self.articleLinks + articleLinks

                try:
                    # visit the next page of the website's search page
                    self.website.nextPage()

                # if there is an error in connecting to the next page, note it in the error log
                except NextPageException:
                    errorLog = open("errorLog.txt", "a+")
                    errorLog.write("Failed to query next page for:   " + self.baseUrl + "\n")
                    errorLog.close()

        # increment the article count by the number of valid article links retrieved
        self.articleCount = self.articleCount + len(self.articleLinks)

        # call to store the article links in the Urls collection
        self.storeInUrlsCollection(self.articleLinks)

    # Return the links contained in the current page of the Website object
    def getPageLinks(self):

        # set page to beautiful soup representation of the current web page
        page = self.website.getCurrentPage()

        # get links from the page
        pageLinks = page.find_all('a', href=True)

        links = []

        for link in pageLinks:
            link = link['href']
            if link not in links:
                links.append(link)

        return links

    # Use the newspaper library to populate the articleLinks attribute with recent article links. Store
    # these links in the Urls collection and increment the article count by the number of articles retrieved
    def crawlRecentArticles(self):

        # build the newspaper website
        # memoize_articles=False param to not use caching
        links = newspaper.build(self.baseUrl, memoize_articles=False)

        # append article to articleLinks
        for article in links.articles:
            self.articleLinks.append(article.url)

        # store article urls in the Urls collection
        self.storeInUrlsCollection(self.articleLinks)

        # increment article count by the number of links retrieved
        self.articleCount = self.articleCount + len(links.articles)

    # Filter urls in the urls argument for only article urls. Make use of urlChecker.valid_url from the
    # newspaper library
    def filterLinksForArticles(self, urls):
        validArticleUrls = []
        for url in urls:
            # some links on source web pages only contain the subdomains and not the entire domain, therefore
            # prepend the base url to the url
            if "http" not in url:
                url = self.baseUrl + url

            # if the the url doesn't containt a certain number of sub folders, it's definitely not an
            # article url
            urlSplit = url.split("/")
            if len(urlSplit) < 5:
                continue

            # validate url to make sure it is an article url before appending to the validArticleUrls list
            if urlChecker.valid_url(url):
                validArticleUrls.append(url)

        return validArticleUrls

    # Manually retrieve article links for websites that are incompatible with the urlChecker.valid_url
    # function
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

    # Set the json file containing websites and their attributes
    def setWebsitesJsonFile(self, jsonFile):
        self.websitesJsonFile = jsonFile

    # Set the base url of the website (as in stripped of any subdomains)
    def setBaseUrl(self, url):
        self.baseUrl = url

    # Set the list of keywords to be used for searching
    def setKeywords(self, keywords):
        self.keywords = keywords

    # Return the list of keywords used for searching
    def getKeywords(self):
        return self.keywords

    # Set the url search query structure used for searching
    def setSearchQueryStructure(self, query):
        self.searchQuery = query

    # Return the list of article links retrieved by the crawler
    def getArticleLinks(self):
        return self.articleLinks

    # Return the number of article links retrieved by the crawler
    def getArticleCount(self):
        return self.articleCount

    # Store the article urls in the Urls collection
    def storeInUrlsCollection(self, urls):
        for url in urls:
            try:
                database.urls(url=url).save()
            except:
                pass