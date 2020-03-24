import requests
from bs4 import BeautifulSoup as soup
import json
from selenium import webdriver
from sys import platform
from selenium.webdriver.chrome.options import Options
import os

class Website:
    def __init__(self, url):
        self.baseUrl = url
        self.currentPageNum = 0
        self.currentPage = soup(requests.get(self.baseUrl).content, "html.parser")
        self.currentUrl = self.baseUrl
        self.currentKey = ""

        # TODO: make sure openning websites.json
        with open('websites.json') as data_file:
            self.websites = json.load(data_file)
            data_file.close()

        # TODO: add custom exception for website not found
        for website, attributes in self.websites.items():
            if website in self.baseUrl:
                self.searchQuery = attributes["searchQuery"]
                self.nextPageType = attributes["nextPage"]

        if self.nextPageType == 3 or self.nextPageType == 4:
            self.setDriver()

    def getPage(self, key):
        query = self.searchQuery.replace("PEATKEY", key).replace("PEATPAGE", str(self.currentPageNum))
        self.currentUrl = query
        page = requests.get(query)
        return soup(page.content, "html.parser")

    def searchForKey(self, key):
        self.currentKey = key
        self.currentPage = self.getPage(key)
        self.currentPageNum = 1

    def nextPage(self):
        if self.nextPageType == 1:
            self.currentPageNum = self.currentPageNum + 1
            self.currentPage = self.getPage(self.currentKey)

        # TODO: make sure this is working properly
        elif self.nextPageType == 2:
            if self.currentPageNum == 1:
                self.currentPageNum = 25
            else:
                self.currentPageNum = self.currentPageNum + 25
                self.currentPage = self.getPage(self.currentKey)

        elif self.nextPageType == 3:
            self.scrollPage()

        else:
            self.currentPageNum = self.currentPageNum + 1
            self.nextPageSelenium()

    def nextPageSelenium(self):

        self.driver.find_element_by_xpath(
            """//*[@id="___gcse_0"]/div/div/div/div[5]/div[2]/div/div/div[2]/div/div
            ["""+str(self.currentPageNum)+"""]"""
        ).click()

    def setDriver(self):
        if platform == "darwin":
            chromeDriverPath = os.path.abspath(os.getcwd()) + "/chromedriver_79_mac"
        else:
            # TODO: download chrome driver for windows
            chromeDriverPath = os.path.abspath(os.getcwd()) + "/chromedriver_win32.exe"

        options = Options()
        # options.add_argument('--headless')
        self.driver = webdriver.Chrome(chromeDriverPath, options=options)
        self.driver.get(self.currentUrl)

    def scrollPage(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        self.currentPage = soup(self.driver.page_source, 'html.parser')
        self.currentPageNum = self.currentPageNum + 1

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

    def getDriver(self):
        return self.driver

    def getCurrentPageNum(self):
        if self.nextPageType == 1:
            return self.currentPageNum
        elif self.nextPageType == 2:
            if self.currentPageNum == 1:
                return 1
            else:
                return int(self.currentPageNum/25 + 1)
        elif self.nextPageType == 3:
            return self.currentPageNum

    def getCurrentUrl(self):
        return self.currentUrl

    def getCurrentKey(self):
        return self.currentKey