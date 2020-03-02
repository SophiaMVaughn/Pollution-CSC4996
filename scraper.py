import requests
from bs4 import BeautifulSoup as soup
from dateutil import parser
import newspaper
import database
import sys
from crawler import Crawler


class Scraper(Crawler):
    def __init__(self):
        super().__init__()
        self.titles = []
        self.scrapedArticles = []

    def scrapeAll(self):
        for article in self.articleLinks:
            print("scraping: ",article)
            self.scrape(article)

    def scrape(self, url):
        article = newspaper.Article(url)
        article.download()
        article.parse()

        page = requests.get(url)
        soupPage = soup(page.content, 'html.parser')

        if self.scrapeTitle(article) not in self.titles:

            article = {
                "url": url,
                "title": self.scrapeTitle(article),
                "publishingDate": self.scrapePublishingDate(soupPage),
                "body": self.scrapeBody(article)
            }

            self.scrapedArticles.append(article)
            self.titles.append(article["title"])

    def scrapeTitle(self, newspaperArticleObj=None):
        title = newspaperArticleObj.title
        if title is None:
            return ""
        else:
            return title

    def scrapePublishingDate(self, soupPage=None):
        # TODO: improve
        date = ""
        if soupPage.find("time", {"itemprop": "datePublished"}) is not None:
            date = soupPage.find("time", {"itemprop": "datePublished"})
        elif soupPage.find("span", {"class": "byline__time"}) is not None:
            date = soupPage.find("span", {"class": "byline__time"})
        elif soupPage.find("time"):
            date = soupPage.find("time")
        elif soupPage.find("h6") is not None:
            date = soupPage.find("h6")
            date = date.get_text()
            date = date.split("|")[1]
        elif soupPage.find("p") is not None:
            date = soupPage.find("p")

        try:
            return self.normalizeDate(date.get_text().strip())
        except:
            print("[-] Exception: could not formate date")
            return ""

    def scrapeBody(self, newspaperArticleObj=None):
        body = newspaperArticleObj.text
        if body is None:
            return ""
        else:
            return body

    def normalizeDate(self, date):
        d = parser.parse(date)
        return d.strftime("%m/%d/%Y")

    def getScrapedArticles(self):
        return self.scrapedArticles