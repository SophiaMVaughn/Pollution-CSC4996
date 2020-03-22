import requests
from bs4 import BeautifulSoup as soup
import database
import newspaper
from newspaper import urls as urlChecker
from textColors import bcolors
import json
import sys
from scraper import Scraper
import datetime
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
        self.setDriver(self.baseUrl)

        with open('websitesTesting.json') as data_file:
            self.websites = json.load(data_file)
            data_file.close()

        for website, attributes in self.websites.items():
            if website in self.baseUrl:
                self.searchQuery = attributes["searchQuery"]

    def getPage(self, key):
        query = self.searchQuery.replace("PEATKEY", key).replace("PEATPAGE", str(self.currentPageNum))
        self.setDriver(query)
        self.currentUrl = query
        page = requests.get(query)
        return soup(page.content, "html.parser")

    def searchForKey(self, key):
        self.currentPage = self.getPage(key)
        self.currentPageNum = 0

    def nextPage(self, key):
        self.currentPage = self.getPage(key)
        self.currentPageNum = self.currentPageNum + 1

    def getCurrentPage(self):
        return self.currentPage

    def setDriver(self, url):
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
