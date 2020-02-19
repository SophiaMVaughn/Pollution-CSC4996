import requests
from bs4 import BeautifulSoup as soup
from dateutil import parser
import database
from textColors import bcolors

################################################
#                Scraper Class                 #
################################################

class Scraper:
    def __init__(self, url, websiteObjList):
        self.articleURL = url
        self.websiteObjList = websiteObjList
        self.articleTitle = ""
        self.articleBody = []
        self.articleDate = ""

        websiteName = url.split("www.")[1].split(".com")[0]

        for website in websiteObjList:
            if websiteName == website.getWebsiteName():
                self.website = website
                self.scrape()

    def scrape(self):
        # print(bcolors.OKGREEN + "[+]" + bcolors.ENDC + " Scraping " + self.articleURL)
        page = requests.get(self.articleURL)
        soup_page = soup(page.content, 'html.parser')

        try:
            # scrape article title
            self.articleTitle = soup_page.find_all(self.website.getTitleTag())[0].get_text()
        except IndexError:
            print(bcolors.FAIL + "[-] Could not retrieve title for " + self.articleURL + bcolors.ENDC)
            self.articleTitle = "Empty"

        # scape article body
        body = soup_page.find_all(self.website.getBodyTag())

        for line in body:
            self.articleBody.append(line.get_text())

        try:
            # scrape article publishing date
            date = soup_page.find_all(self.website.getPublishingDateTag())[0].get_text().strip()
            self.articleDate = self.normalizeDate(date)
        except IndexError:
            print(bcolors.FAIL + "[-] Could not retrieve date for " + self.articleURL + bcolors.ENDC)
            self.articleDate = "Empty"

    def storeInDatabase(self):
        try:
            database.Articles(
                publishingDate=self.getArticleDate(),
                title=self.getArticleTitle(),
                url=self.getArticleURL()
            ).save()
        except:
            # print(bcolors.WARNING + "[-] Duplicate URL: " + self.getArticleURL() + bcolors.ENDC)
            pass

    def normalizeDate(self, date):
        d = parser.parse(date)
        return d.strftime("%m/%d/%Y")

    def getArticleTitle(self):
        return self.articleTitle

    def getArticleDate(self):
        return self.articleDate

    def getArticleBody(self):
        return self.articleBody

    def getArticleURL(self):
        return self.articleURL







