import database
from textColors import bcolors
from crawler import  Crawler
from scraper import Scraper
from tqdm import tqdm
import json
from exceptions import WebsiteFailedToInitialize

class ScraperInterface:
    def __init__(self, keywords, websitesJsonFile="websites.json"):
        self.keywords = keywords
        self.websites = []
        self.articleUrls = []
        self.articleObjs = []
        self.articleCount = 0
        self.websitesJsonFile = websitesJsonFile

        self.pullWebsites()
        self.crawl()


    def crawl(self):
        for website in self.websites:
            links = []
            try:
                crawler = Crawler(website, self.keywords, 2)
                self.articleCount = self.articleCount + crawler.getArticleCount()
                for url in crawler.getArticleLinks():
                    links.append(url)
                    self.articleUrls.append(url)
            # TODO: handle the exception
            except WebsiteFailedToInitialize:
                pass

            self.scrape(links)

        print("\r" + bcolors.OKGREEN + "[+] All articles scraped" + bcolors.ENDC)

    def scrape(self, urls):
        loop = tqdm(total=len(urls), position=0, leave=False)
        for url in urls:
            loop.set_description("\t[+] Scraping...".format(url))
            loop.update(1)
            try:
                scraper = Scraper(url)
                self.articleObjs.append(scraper.getScrapedArticle())
            except:
                print("Could not scrape:  " + str(url))
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
            errorLog.write("\nCould not add article:   " + article['url'])

    def storeInIncidentsCollection(self, chems, date, location, statement, links):
        if len(location) == 0:
            database.Errors(
                chems=chems,
                day=date,
                loc=location,
                offStmt=statement,
                artLinks=links,
                errorMessage="No location found."
            ).save()
            print("Passed - no loc")
        elif len(chems)==0:
            database.Errors(
                chems=chems,
                day=date,
                loc=location,
                offStmt=statement,
                artLinks=links,
                errorMessage="No chemicals found."
            ).save()
            print("Passed - no chem")
        else:
            try:
                database.Incidents(
                    chemicals=chems,
                    date=date,
                    location=location,
                    officialStatement=statement,
                    articleLinks=links
                ).save()
                print("SAVED")
            except:
                pass

# errorLog = open("errorLog.txt", "a+")
# errorLog.write("Error scraping article: " + self.url + "\n")
# errorLog.close()
