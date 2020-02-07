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
        self.articleDate = ""

        self.scrape()

    # From raw HTML, retrieve article title, publishing date, and body
    def scrape(self):
        print("[+] Scraping " + str(self.articleURL))
        page = requests.get(self.articleURL)
        soup_page = soup(page.content, 'html.parser')

        # scrape article title
        self.articleTitle = soup_page.find_all(class_="util-bar-share-summary-title")[0].get_text()

        # scape article body
        body = soup_page.find_all(class_="p-text")

        for paragraph in body:
            self.articleBody.append(paragraph.get_text())

        # scrape publishing date
        url_split = self.articleURL.split("/")
        date = url_split[-5] + "/" + url_split[-4] + "/" + url_split[-6]
        self.setArticleDate(date)

    # stores scraped data in database
    def storeInDatabase(self):
        incident = database.Incidents(
            articleDate=self.getArticleDate(),
            articleTitle=self.getArticleTitle(),
            url=self.getArticleURL()
        ).save()

    # set the article date to date param
    def setArticleDate(self, date):
        self.articleDate = date

    # set the article title to title param
    def setArticleTitle(self, title):
        self.articleTitle = title

    # set the article url to url param
    def setURL(self, url):
        self.articleURL = url

    # set the article body to body param
    def setArticleBody(self, body):
        self.articleBody = body

    # return the article publishing date
    def getArticleDate(self):
        return self.articleDate

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
