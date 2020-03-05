import requests
from bs4 import BeautifulSoup as soup
from dateutil import parser
import sys
from crawler import Crawler
from textColors import bcolors
from tqdm import tqdm
import re


class Scraper():
    def __init__(self, url):
        self.titles = []
        self.scrapedArticles = []

        self.article = {
            "url": url,
            "title": None,
            "publishingDate": None,
            "body": None
        }

        self.scrape(url)

    def scrape(self, url):
        page = requests.get(url)
        soupPage = soup(page.content, 'html.parser')

        if self.scrapeTitle(soupPage) not in self.titles:

            self.article['title'] = self.scrapeTitle(soupPage)
            self.article['publishingDate'] = self.scrapePublishingDate(soupPage)
            self.article['body'] = self.scrapeBody(soupPage)

            if self.article['publishingDate'] == "":
                errorLog = open("errorLog.txt", "a+")
                errorLog.write("could not format date for article: " + self.article['url'] + "\n")
                errorLog.close()

            self.scrapedArticles.append(self.article)
            self.titles.append(self.article["title"])

    def scrapeTitle(self, soupPage=None):
        if soupPage is None:
            return ""
        else:
            return soupPage.find("title").get_text().strip()

    def scrapePublishingDate(self, soupPage=None):
        # TODO: improve
        date = ""
        if soupPage.find("time", {"itemprop": "datePublished"}) is not None:
            date = soupPage.find("time", {"itemprop": "datePublished"}).get_text().strip()
        elif soupPage.find("span", {"class": "byline__time"}) is not None:
            date = soupPage.find("span", {"class": "byline__time"}).get_text().strip()
        elif soupPage.find("time"):
            date = soupPage.find("time").get_text().strip()
        elif soupPage.find("h6") is not None:
            date = soupPage.find("h6")
            date = date.get_text().strip()
            date = date.split("|")[1]
        elif soupPage.find("p") is not None:
            date = soupPage.find("p").get_text().strip()

        try:
            return self.normalizeDate(date)
        except:
            return ""

    def scrapeBody(self, soupPage=None):
        if soupPage is None:
            return ""
        else:
            body = ""
            bodyList = soupPage.find_all("p")
            for lines in bodyList:
                body = body + " " + lines.get_text()
            body = re.sub("\s\s+" , " ", body)
            return body

    def normalizeDate(self, date):
        d = parser.parse(date)
        return d.strftime("%m/%d/%Y")

    def getScrapedArticle(self):
        return self.article
