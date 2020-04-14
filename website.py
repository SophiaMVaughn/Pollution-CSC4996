import requests
from bs4 import BeautifulSoup as soup
import json
from exceptions import WebsiteFailedToInitialize, NextPageException


class Website:
    def __init__(self, url, websitesJsonFile="websites.json"):
        self.baseUrl = url
        self.websitesJsonFile = websitesJsonFile
        self.currentPageNum = 0

        try:
            self.currentPage = soup(requests.get(self.baseUrl).content, "html.parser")
        except:
            raise WebsiteFailedToInitialize(self.baseUrl)

        self.currentUrl = self.baseUrl
        self.currentKey = ""

        with open(self.websitesJsonFile) as data_file:
            self.websites = json.load(data_file)
            data_file.close()

        for website, attributes in self.websites.items():
            if website in self.baseUrl:
                self.searchQuery = attributes["searchQuery"]
                self.nextPageType = attributes["nextPage"]

    def getPage(self, key):
        self.currentUrl = self.searchQuery.replace("PEATKEY", key).replace("PEATPAGE", str(self.currentPageNum))
        page = requests.get(self.currentUrl)
        return soup(page.content, "html.parser")

    def searchForKey(self, key):
        self.currentKey = key
        self.currentPage = self.getPage(key)
        self.currentPageNum = 1

    def nextPage(self):
        try:
            if self.nextPageType == 1:
                self.currentPageNum = self.currentPageNum + 1
                self.currentPage = self.getPage(self.currentKey)

            elif self.nextPageType == 2:
                if self.currentPageNum == 1:
                    self.currentPageNum = 25
                else:
                    self.currentPageNum = self.currentPageNum + 25
                    self.currentPage = self.getPage(self.currentKey)
        except:
            raise NextPageException(self.currentUrl)

    def resetPageToBaseUrl(self):
        self.currentUrl = self.baseUrl
        self.currentPage = soup(requests.get(self.baseUrl).content, "html.parser")
        self.currentPageNum = 0

    def resetPageToFirstSearchPage(self):
        self.currentUrl = self.searchQuery.replace("PEATPAGE", "1")
        self.currentPage = soup(requests.get(self.currentUrl).content, "html.parser")
        self.currentPageNum = 1

    def getCurrentPage(self):
        return self.currentPage

    def setWebsitesJsonFile(self, jsonFile):
        self.websitesJsonFile = jsonFile

    def getCurrentPageNum(self):
        if self.nextPageType == 1:
            return self.currentPageNum
        elif self.nextPageType == 2:
            if self.currentPageNum == 1:
                return 1
            else:
                return int(self.currentPageNum/25 + 1)

    def getCurrentUrl(self):
        return self.currentUrl

    def getCurrentKey(self):
        return self.currentKey