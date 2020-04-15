import requests
from bs4 import BeautifulSoup as soup
from dateutil import parser
import re
from newspaper import Article


# The Scraper class serves to retrieve various attributes (article title, publishing date, and body)
# from the give article passed to the object

class Scraper:

    # Constructor for the Scraper class
    def __init__(self, url):
        self.scrapedArticles = []
        self.newspaperArticle = None

        try:
            # setup Article object from the newspaper library
            self.newspaperArticle = Article(url)
            self.newspaperArticle.download()
            self.newspaperArticle.parse()

        # if error occurs during instantiation and download of the article, make note of the error in
        # the error log
        except:
            errorLog = open("errorLog.txt", "a+")
            errorLog.write("Could not download article:   " + url + "\n")
            errorLog.close()

        # initialize the dictionary object to hold the scraped values
        self.article = {
            "url": url,
            "title": None,
            "publishingDate": None,
            "body": None
        }

        self.scrape(url)

    # Scrape the article for the title, publishing date, and body and set the dictionary values to
    # these attributes
    def scrape(self, url):

        # GET request to url
        page = requests.get(url)

        # create beautiful soup object from the page's html source code
        soupPage = soup(page.content, 'html.parser')

        # set the title, date, and body values of the article dictionary to the scraped title, date,
        # and body of the article, respectively
        self.article['title'] = self.scrapeTitle(soupPage)
        self.article['publishingDate'] = self.scrapePublishingDate(soupPage)
        self.article['body'] = self.scrapeBody(soupPage)

        # if article publishing date is empty, note it in the error log
        if self.article['publishingDate'] == "":
            errorLog = open("errorLog.txt", "a+")
            errorLog.write("could not format date for article:   " + self.article['url'] + "\n")
            errorLog.close()

        # add scraped article dictionary to the scrapedArticles list
        self.scrapedArticles.append(self.article)

    # Return article title
    def scrapeTitle(self, soupPage=None):
        if soupPage is None:
            return ""
        else:
            # return the string contained in the <title> tage of the page html
            return soupPage.find("title").get_text().strip()

    # Return article publishing date
    def scrapePublishingDate(self, soupPage=None):
        date = ""

        # first see if newspaper library can retrieve date, otherwise continue manually
        if self.newspaperArticle.publish_date is not None:
            date = self.newspaperArticle

        # publishing date could be in one of various different tags/classes
        elif soupPage.find("time", {"itemprop": "datePublished"}) is not None:
            date = soupPage.find("time", {"itemprop": "datePublished"}).get_text().strip()
        elif soupPage.find("span", {"class": "byline__time"}) is not None:
            date = soupPage.find("span", {"class": "byline__time"}).get_text().strip()
        elif soupPage.find("time"):
            date = soupPage.find("time").get_text().strip()
        elif soupPage.find("h6") is not None:
            date = soupPage.find("h6")
            date = date.get_text().strip()
            try:
                date = date.split("|")[1]
            except:
                return ""
        elif soupPage.find("p") is not None:
            date = soupPage.find("p").get_text().strip()

        try:
            # try to normalize the date
            return self.normalizeDate(date)

        # if exception is thrown, then date was probably not valid
        except:
            return ""

    # Return article body
    def scrapeBody(self, soupPage=None):
        if soupPage is None:
            return ""
        else:
            body = ""
            bodyList = soupPage.find_all("p")

            # turn array of body lines into one line
            for lines in bodyList:
                body = body + " " + lines.get_text()
            body = re.sub("\s\s+" , " ", body)
            return body

    # Convert the publishing date retrieved to a standard format (ex. 08/24/2019)
    def normalizeDate(self, date):
        d = parser.parse(str(date))
        return d.strftime("%m/%d/%Y")

    # Return the dictionary object that contains the article's scraped attributes
    def getScrapedArticle(self):
        return self.article
