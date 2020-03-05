import requests
from bs4 import BeautifulSoup as soup
from dateutil import parser
import sys
from crawler import Crawler
from textColors import bcolors
from tqdm import tqdm
import re


class Scraper(Crawler):
    def __init__(self):
        super().__init__()
        self.titles = []
        self.scrapedArticles = []

    def scrape(self):

        loop = tqdm(total=len(self.articleLinks), position=0, leave=False)

        for articleUrl in self.articleLinks:

            loop.set_description("\t[+] Scraping...".format(articleUrl))
            loop.update(1)

            # print("\r\t" + bcolors.OKGREEN + "[+]" + bcolors.ENDC + " Scraping " + articleUrl, end="")
            # sys.stdout.flush()

            try:
                self.scrapePage(articleUrl)
            except:
                errorLog = open("errorLog.txt", "a+")
                errorLog.write("Error scraping article: " + articleUrl + "\n")
                errorLog.close()
                pass

        loop.close()

    def scrapePage(self, url):
        page = requests.get(url)
        soupPage = soup(page.content, 'html.parser')

        if self.scrapeTitle(soupPage) not in self.titles:

            article = {
                "url": url,
                "title": self.scrapeTitle(soupPage),
                "publishingDate": self.scrapePublishingDate(soupPage),
                "body": self.scrapeBody(soupPage)
            }

            if article['publishingDate'] == "":
                errorLog = open("errorLog.txt", "a+")
                errorLog.write("could not format date for article: " + article['url'] + "\n")
                errorLog.close()

            self.scrapedArticles.append(article)
            self.titles.append(article["title"])


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

    def getScrapedArticles(self):
        return self.scrapedArticles