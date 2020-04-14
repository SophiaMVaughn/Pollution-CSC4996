import database
from textColors import bcolors
from crawler import  Crawler
from scraper import Scraper
from tqdm import tqdm
import json
from exceptions import WebsiteFailedToInitialize

from dateutil import parser
from datetime import date
from datetime import datetime

class ScraperInterface:
    def __init__(self, keywords, searchPageLimit=2, websitesJsonFile="websites.json"):
        self.keywords = keywords
        self.websites = []
        self.articleUrls = []
        self.articleObjs = []
        self.articleCount = 0
        self.websitesJsonFile = websitesJsonFile
        self.searchPageLimit = searchPageLimit

        self.pullWebsites()
        self.crawl()


    def crawl(self):
        for website in self.websites:
            links = []
            try:
                crawler = Crawler(url=website, keywords=self.keywords,
                                  searchPageLimit=self.searchPageLimit,
                                  websitesJsonFile=self.websitesJsonFile)
                self.articleCount = self.articleCount + crawler.getArticleCount()
                for url in crawler.getArticleLinks():
                    links.append(url)
                    self.articleUrls.append(url)
            # TODO: handle the exception
            except WebsiteFailedToInitialize:
                errorLog = open("errorLog.txt", "a+")
                errorLog.write("\nCould not crawl:  " + website)

            self.scrape(links)

        print("\r" + bcolors.OKGREEN + "[+] All articles retrieved" + bcolors.ENDC)

    def scrape(self, urls):
        loop = tqdm(total=len(urls), position=0, leave=False)
        for url in urls:
            loop.set_description("\t[+] Scraping...".format(url))
            loop.update(1)
            try:
                scraper = Scraper(url)
                self.articleObjs.append(scraper.getScrapedArticle())
            except:
                errorLog = open("errorLog.txt", "a+")
                errorLog.write("\nCould not scrape:  " + url)
        loop.close()

    def setWebsitesJsonFile(self, jsonFile):
        self.websitesJsonFile = jsonFile

    def pullWebsites(self):
        # TODO: make sure openning websites.json
        with open(self.websitesJsonFile) as data_file:
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
            database.articles(
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
            errorLog.write("\nCould not add article:   " + article['url'])


#this function takes all of the information about an incident
#and stores it in either the error or incidents database
    def storeInIncidentsCollection(self, chems, date, location, statement, links):
        if date =="": #this date will make the front end crash
            #so we put it in the error database
            database.errors(
                chems=chems,
                day=date,
                loc=str(location),
                offStmt=statement,
                artLinks=links,
                errorMessage="Bad date."
            ).save()
            print("Passed - Bad date")
            return
        else: 
            try:
                #if the date is not blank, test if it can be formatted,
                #if it can't, it will also crash the front end
                datetime.strptime(date, '%m/%d/%Y')
            except ValueError: #if formatting failed
                #insert into the error database
                database.errors(
                    chems=chems,
                    day=date,
                    loc=str(location),
                    offStmt=statement,
                    artLinks=links,
                    errorMessage="Bad date."
                ).save()
                print("Passed - Bad date")
                return
        
        
        if len(chems)==0: #if there were no chemicals
            database.errors( #insert it into the error database
                chems=chems,
                day=date,
                loc=str(location),
                offStmt=statement,
                artLinks=links,
                errorMessage="No chemicals found."
            ).save()
            print("Passed - no chem")
        elif len(location) == 0: #if there was no location
            database.incidents( #insert it into the incidents database
                    chemicals=chems,
                    date=date,
                    location="none", #but with a special location
                    officialStatement=statement,
                    articleLinks=links
                ).save()
            print("Saved - no loc")
        else: #if all of these situations did not happen
            try:
                database.incidents( #insert as a normal incident
                    chemicals=chems,
                    date=date,
                    location=str(location),
                    officialStatement=statement,
                    articleLinks=links
                ).save()
                print("SAVED")
            except:
                pass

# errorLog = open("errorLog.txt", "a+")
# errorLog.write("Error scraping article: " + self.url + "\n")
# errorLog.close()
