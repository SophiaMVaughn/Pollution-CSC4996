from websites import *
import database
import sys
from textColors import bcolors
from crawler import  Crawler
from scraper import Scraper
from tqdm import tqdm
import time
import json

class ScraperInterface:
    def __init__(self, keywords):
        self.keywords = keywords
        self.websites = []
        self.articleUrls = []
        self.articleObjs = []
        self.articleCount = 0

        self.pullWebsites()
        self.crawl()


    def crawl(self):
        for website in self.websites:
            links = []
            crawler = Crawler(website, self.keywords)
            self.articleCount = self.articleCount + crawler.getArticleCount()
            for url in crawler.getArticleLinks():
                links.append(url)
                self.articleUrls.append(url)

            self.scrape(links)

        print("\r" + bcolors.OKGREEN + "[+] All articles scraped" + bcolors.ENDC)

    def scrape(self, urls):
        loop = tqdm(total=len(urls), position=0, leave=False)
        for url in urls:
            loop.set_description("\t[+] Scraping...".format(url))
            loop.update(1)
            scraper = Scraper(url)
            self.articleObjs.append(scraper)
        loop.close()

    def pullWebsites(self):
        with open('websites.json') as data_file:
            data = json.load(data_file)

        for website, attributes in data.items():
            self.websites.append(attributes['url'])

    def getArticleCount(self):
        return self.articleCount

    def getArticleUrl(self):
        return self.articleUrls

    def getScrapedArticles(self):
        return self.articleObjs

    def storeInArticlesCollection(self, article):
        try:
            database.Articles(
                url=article['url'],
                title=article['title'],
                publishingDate=article['publishingDate']
            ).save()

            articleBodies = open("articleBodies.txt", "a+")
            articleBodies.write("url: " + article['url'] + "\n")
            articleBodies.write(article['body'] + "\n")
            articleBodies.write("\n" + "#"*100 + "\n")
            articleBodies.close()
        except:
            errorLog = open("errorLog.txt", "a+")
            errorLog.write("\ncould not add article: " + article['url'])
            # raise
            pass

    def storeInIncidentsCollection(self, chems, date, location, statement, links):
        try:
            database.Incidents(
                chemicals=chems,
                date=date,
                location=location,
                officialStatement=statement,
                articleLinks=links
            ).save()
        except:
            pass

# errorLog = open("errorLog.txt", "a+")
# errorLog.write("Error scraping article: " + self.url + "\n")
# errorLog.close()