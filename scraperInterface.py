import database
from textColors import bcolors
from crawler import  Crawler
from scraper import Scraper
from tqdm import tqdm
import json
from exceptions import WebsiteFailedToInitialize
from datetime import datetime


# The ScraperInterface class serves to abstract the crawler, scraper, and database implementations from the
# main script.

class ScraperInterface:

    # Constructor for the ScraperInterface class
    def __init__(self, keywords, searchPageLimit=2, websitesJsonFile="websites.json"):

        # iinitialize class attributes
        self.keywords = keywords
        self.websites = []
        self.articleUrls = []
        self.articleObjs = []
        self.articleCount = 0
        self.websitesJsonFile = websitesJsonFile
        self.searchPageLimit = searchPageLimit

        self.pullWebsites()
        self.crawl()

    # The crawl method creates a Crawler object for each website. The article urls retrieved by each Crawler
    # object is then appended to the 'links' list, which is then passed to the scrape method.  Any websites
    # that fail to be connected to will be noted in the error log.
    def crawl(self):
        # iterate through list of website urls
        for website in self.websites:

            # hold urls retrieved by Crawler objects
            links = []

            try:

                # instantiate Crawler object
                crawler = Crawler(url=website, keywords=self.keywords,
                                  searchPageLimit=self.searchPageLimit,
                                  websitesJsonFile=self.websitesJsonFile)

                # increment counter holding the number of articles retrieved
                self.articleCount = self.articleCount + crawler.getArticleCount()

                # append article urls retrieved by the crawler to the articleUrls list attribute
                for url in crawler.getArticleLinks():
                    links.append(url)
                    self.articleUrls.append(url)

            # catch exception thrown by Crawler if the crawler cannot establish connection to the website
            # and note the error in the error log
            except WebsiteFailedToInitialize:
                errorLog = open("errorLog.txt", "a+")
                errorLog.write("\nCould not crawl:  " + website)

            # call the scrape method and pass list of urls as the argument
            self.scrape(links)

        print("\r" + bcolors.OKGREEN + "[+] All articles retrieved" + bcolors.ENDC)

    # The scrape method takes the list of urls passed to it as an argument and creates a Scraper object
    # for each url. For each Scraper object, a dictionary of article attributes is returned and appended
    # to the articleObjs attributes.
    def scrape(self, urls):

        # for the progress bar to show how many articles out the total number in the urls list have
        # been scraped
        loop = tqdm(total=len(urls), position=0, leave=False)

        for url in urls:

            # set the progress text and update
            loop.set_description("\t[+] Scraping...".format(url))
            loop.update(1)

            try:
                scraper = Scraper(url)
                self.articleObjs.append(scraper.getScrapedArticle())

            # catch exception if error occurs during scrape and note it in the error log
            except:
                errorLog = open("errorLog.txt", "a+")
                errorLog.write("\nCould not scrape:  " + url)

        # terminate the progress bar
        loop.close()

    # Set file used to pull websites urls and attributes from.
    def setWebsitesJsonFile(self, jsonFile):
        self.websitesJsonFile = jsonFile

    # Open the json file specified by the websitesJsonFile attribute, iterate through the websites in the
    # file and append them to the websites attribute.
    def pullWebsites(self):
        with open(self.websitesJsonFile) as data_file:
            data = json.load(data_file)

        # append only the url for each website in the json file to the websites attribute
        for website, attributes in data.items():
            self.websites.append(attributes['url'])

    # Return the number of articles crawled.
    def getArticleCount(self):
        return self.articleCount

    # Return the list of urls crawled.
    def getArticleUrls(self):
        return self.articleUrls

    # Return the list of dictionary objects containing scraped attributes for each article.
    def getScrapedArticles(self):
        return self.articleObjs

    # Store the attributes (url, title, publishing date) of the article specified by the article object
    # 'article' into the Articles collection. If an error occurs during this process, it is noted in the
    # error log.
    def storeInArticlesCollection(self, article):
        try:
            # store in articles collection
            database.articles(
                url=article['url'],
                title=article['title'],
                publishingDate=article['publishingDate']
            ).save()

            # append the url and body of the article to the articleBody text file
            articleBodies = open("articleBodies.txt", "a+")
            articleBodies.write("url: " + article['url'] + "\n")
            articleBodies.write(article['body'] + "\n")
            articleBodies.write("\n" + "#"*100 + "\n")
            articleBodies.close()

        # catch error while inserting into the database and note it in the error log file
        except:
            errorLog = open("errorLog.txt", "a+")
            errorLog.write("\nCould not add article:   " + article['url'])

    # Store attributes (chemicals, date, location, official statement, article links) of the contamination
    # incident in the Incidents collection. If an error occurs during this process, it is noted in the
    # error log.
    def storeInIncidentsCollection(self, chems, date, location, statement, links):

        # this date will make the front end crash so we put it in the error database
        if date == "":
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
                # if the date is not blank, test if it can be formatted, if it can't, it will also
                # crash the front end
                datetime.strptime(date, '%m/%d/%Y')

            # if formatting failed insert into the error database
            except ValueError:
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

        # if there were no chemicals
        if len(chems) == 0:
            # insert it into the error database
            database.errors(
                chems=chems,
                day=date,
                loc=str(location),
                offStmt=statement,
                artLinks=links,
                errorMessage="No chemicals found."
            ).save()
            print("Passed - no chem")

        # if there was no location
        elif len(location) == 0:
            # insert it into the incidents database
            database.incidents(
                    chemicals=chems,
                    date=date,
                    location="none", # but with a special location
                    officialStatement=statement,
                    articleLinks=links
                ).save()
            print("Saved - no loc")

        # if all of these situations did not happen
        else:
            try:
                # insert as a normal incident
                database.incidents(
                    chemicals=chems,
                    date=date,
                    location=str(location),
                    officialStatement=statement,
                    articleLinks=links
                ).save()
                print("SAVED")
            except:
                pass
