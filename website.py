import requests
from bs4 import BeautifulSoup as soup
import json
from exceptions import WebsiteFailedToInitialize, NextPageException


# The Website class serves as an abstraction for websites, separating website functionality from the crawler

class Website:

    # Constructor for the Website class
    def __init__(self, url, websitesJsonFile="websites.json"):
        self.baseUrl = url
        self.websitesJsonFile = websitesJsonFile
        self.currentPageNum = 0

        try:
            # set current page to the beautiful soup representation of the base webpage
            self.currentPage = soup(requests.get(self.baseUrl).content, "html.parser")

        # if there is an error with the initial connection, raise an exception
        except:
            raise WebsiteFailedToInitialize(self.baseUrl)

        self.currentUrl = self.baseUrl
        self.currentKey = ""

        # open the json file containing websites and their attributes
        with open(self.websitesJsonFile) as data_file:
            self.websites = json.load(data_file)
            data_file.close()

        # set the searchQuery attribute to the appropriate search query structure and set the nextPageType
        # attribute to the appropriate next page type
        for website, attributes in self.websites.items():
            if website in self.baseUrl:
                self.searchQuery = attributes["searchQuery"]
                self.nextPageType = attributes["nextPage"]

    # Return the beautiful soup representation of the current url
    def getPage(self, key):
        # replace the place holder string (PEATKEY and PEATPAGE) with the specific key and page number needed
        self.currentUrl = self.searchQuery.replace("PEATKEY", key).replace("PEATPAGE", str(self.currentPageNum))
        # GET request to url
        page = requests.get(self.currentUrl)
        return soup(page.content, "html.parser")

    # Search for the web page specified by the search key passed to the method
    def searchForKey(self, key):
        self.currentKey = key
        self.currentPage = self.getPage(key)
        self.currentPageNum = 1

    # Search for the next page from the current search page
    def nextPage(self):
        try:
            if self.nextPageType == 1:
                self.currentPageNum = self.currentPageNum + 1
                self.currentPage = self.getPage(self.currentKey)

            elif self.nextPageType == 2:
                # with websites of this class (nextPageType = 2), pages are tracked by article count and
                # they increment by 25. The first page of the search result is technically represented by
                # the value 0, but 0 is used here to denote the base url so I just set it to one
                if self.currentPageNum == 1:
                    self.currentPageNum = 25
                else:
                    self.currentPageNum = self.currentPageNum + 25
                    self.currentPage = self.getPage(self.currentKey)
        except:
            raise NextPageException(self.currentUrl)

    # Set the current page and current url back to the base page and base url, respectively, and reset
    # page number
    def resetPageToBaseUrl(self):
        self.currentUrl = self.baseUrl
        self.currentPage = soup(requests.get(self.baseUrl).content, "html.parser")
        self.currentPageNum = 0

    # Set the current page and current url back to the first search page and first search page url,
    # respectively, and reset page number
    def resetPageToFirstSearchPage(self):
        self.currentUrl = self.searchQuery.replace("PEATPAGE", "1")
        self.currentPage = soup(requests.get(self.currentUrl).content, "html.parser")
        self.currentPageNum = 1

    # Return beautiful soup representation of the current page
    def getCurrentPage(self):
        return self.currentPage

    # Set the json file containing websites and their attributes
    def setWebsitesJsonFile(self, jsonFile):
        self.websitesJsonFile = jsonFile

    # Return the current page number. For websites that use article count as a page reference, adjust the
    # value to represent a page number
    def getCurrentPageNum(self):
        if self.nextPageType == 1:
            return self.currentPageNum
        elif self.nextPageType == 2:
            if self.currentPageNum == 1:
                return 1
            else:
                # websites with nextPageType type = 2 increment page number by 25 articles, so divide by 25 and
                # add 1 to get the intuitive page number
                return int(self.currentPageNum/25 + 1)

    # Return the current url
    def getCurrentUrl(self):
        return self.currentUrl

    # Return the current search key word
    def getCurrentKey(self):
        return self.currentKey