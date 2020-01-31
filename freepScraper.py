# Detroit Free Press Scraper

import requests
from bs4 import BeautifulSoup as soup
import database

class FreepScraper:

    # initialize variables
    def __init__(self, url):
        self.articleURL = url
        self.articleTitle = ""
        self.articleBody = []

        page = requests.get(self.articleURL)
        soup_page = soup(page.content, 'html.parser')
        self.articleTitle = soup_page.find_all(class_="util-bar-share-summary-title")[0].get_text()
        body = soup_page.find_all(class_="p-text")

        for paragraph in body:
            self.articleBody.append(paragraph.get_text())

    # stores scraped data in database
    def storeInDatabase(self):
        incident = database.Incidents(
            url=self.getArticleURL(),
            articleTitle=self.getArticleTitle()
        ).save()

    # set the article title to articleTitle param
    def setArticleTitle(self, articleTitle):
        self.articleTitle = articleTitle

    # set the article url to url param
    def setURL(self, url):
        self.articleURL = url

    # set the article body to body param
    def setArticleBody(self, body):
        self.articleBody = body

    # return the article title
    def getArticleTitle(self):
        return self.articleTitle

    # return the article url
    def getArticleURL(self):
        return self.articleURL

    # return the article body
    def getArticleBody(self):
        return self.articleBody

    # print the article body
    def printArticleBody(self):
        for body in self.articleBody:
            print(body + "\n")