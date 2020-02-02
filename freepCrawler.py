import requests
from bs4 import BeautifulSoup as soup
import time
from selenium import webdriver
import os
from sys import platform


class FreepCrawler():
    # initialize variables and create list of base urls with the different search keywords
    def __init__(self, *keywords):
        self.urls = []
        self.baseURLs = []
        self.keywords = []

        for key in keywords:
            self.keywords.append(key)
            self.baseURLs.append("https://www.freep.com/search/" + key + "/")


    # print all urls that have been crawled
    def printURLs(self):
        for url in self.urls:
            print(url)

    # for each base url, crawl all article links contained in each.  For instance, base url is the search result for polution,
    # so crawlURLs() will retrieve article urls from that page and append them to the urls list
    def crawlURLs(self):
        try:
            for url in self.baseURLs:
                if platform == "darwin":
                    chromeDriverPath = os.path.abspath(os.getcwd()) + "/chromedriver_mac"
                else:
                    chromeDriverPath = os.path.abspath(os.getcwd()) + "/chromedriver_win32.exe"

                driver = webdriver.Chrome(chromeDriverPath)
                driver.get(url)

                withinLastYear = True

                while withinLastYear:
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

                    soup_page = soup(driver.page_source, 'html.parser')
                    articleDates = soup_page.find_all(class_="date-created meta-info-text")

                    for date in articleDates:
                        if "2019" in date.get_text():
                            withinLastYear = False

                    time.sleep(4)

                source = driver.page_source
                soup_page = soup(source, 'html.parser')
                links = soup_page.find_all('a', href=True)

            for link in links:
                if "/story/news/local/michigan/" in link['href']:
                    self.urls.append("https://www.freep.com" + link['href'])

        except requests.exceptions.ConnectionError:
            print("[-] Connection refused: too man requests")


    def getURLs(self):
        return self.urls


    def getURLs(self):
        return self.urls
