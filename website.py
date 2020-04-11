import requests
from bs4 import BeautifulSoup as soup
import json
from selenium import webdriver
from sys import platform
from selenium.webdriver.chrome.options import Options
import os
from exceptions import WebsiteFailedToInitialize, NextPageException, DriverException
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager


class Website:
    def __init__(self, url, driver="chrome", websitesJsonFile="websites.json"):
        self.baseUrl = url
        self.websitesJsonFile = websitesJsonFile

        if driver != "chrome" and driver != "firefox":
            raise DriverException(driver)
        else:
            self.driverType = driver

        self.currentPageNum = 0

        try:
            self.currentPage = soup(requests.get(self.baseUrl).content, "html.parser")
        except:
            raise WebsiteFailedToInitialize(self.baseUrl)

        self.currentUrl = self.baseUrl
        self.currentKey = ""

        # TODO: make sure openning websites.json
        with open(self.websitesJsonFile) as data_file:
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
        try:
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
                self.currentPageNum = self.currentPageNum + 1
                self.scrollPage()

            else:
                self.currentPageNum = self.currentPageNum + 1
                self.nextPageSelenium()
        except:
            raise NextPageException(self.currentUrl)

    def nextPageSelenium(self):
        self.driver.find_element_by_xpath(
            """//*[@id="___gcse_0"]/div/div/div/div[5]/div[2]/div/div/div[2]/div/div
            ["""+str(self.currentPageNum)+"""]"""
        ).click()
        self.currentPage = soup(self.driver.page_source, 'html.parser')

    def setDriver(self):

        # TODO: dead code
        # chromeDriverPath = ""
        # firefoxDriverPath = ""
        #
        # if platform == "win32":
        #     if self.driverType == "chrome":
        #         chromeDriverPath = os.path.abspath(os.getcwd()) + "/Driver/Windows/Chrome/chromedriver.exe"
        #     else:
        #         firefoxDriverPath = os.path.abspath(os.getcwd()) + "/Driver/Windows/Firefox"
        # elif platform == "darwin":
        #     if self.driverType == "chrome":
        #         chromeDriverPath = os.path.abspath(os.getcwd()) + "/Driver/Mac/Chrome/chromedriver"
        #     else:
        #         firefoxDriverPath = os.path.abspath(os.getcwd()) + "/Driver/Mac/Firefox"
        # else:
        #     if self.driverType == "chrome":
        #         chromeDriverPath = os.path.abspath(os.getcwd()) + "/Driver/Linux/Chrome/chromedriver"
        #     else:
        #         firefoxDriverPath = os.path.abspath(os.getcwd()) + "/Driver/Linux/Firefox"

        options = Options()
        options.add_argument('--headless')

        # if self.driverType == "chrome":
        #     self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        #     # self.driver = webdriver.Chrome(executable_path=chromeDriverPath, options=options)

        self.driver = webdriver.Firefox(options=options)
        self.driver.get(self.currentUrl)

    def scrollPage(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        self.currentPage = soup(self.driver.page_source, 'html.parser')

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

    def setDriverType(self, driver):
        if driver != "chrome" and driver != "firefox":
            raise DriverException(driver)
        else:
            self.driverType = driver

    def setWebsitesJsonFile(self, jsonFile):
        self.websitesJsonFile = jsonFile

    def getDriverType(self):
        return self.driverType

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