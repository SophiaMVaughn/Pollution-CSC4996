from websites import *
import database
import sys

class ScraperInterface:
    def __init__(self, keywords):
        self.keywords = keywords
        self.websites = []
        self.validArticles = []
        self.articleCount = 0

        # self.websites.append(Ourmidland(keywords))
        self.websites.append(MarionPress(keywords))
        # self.websites.append(TheCountyPress(keywords))
        # self.websites.append(LakeCountyStar(keywords))
        # self.websites.append(NorthernExpress(keywords))
        # self.websites.append(ManisteeNews(keywords))
        # self.websites.append(MichiganChronicle(keywords))
        # self.websites.append(HarborLightNews(keywords))
        # self.websites.append(TheDailyNews(keywords))
        # self.websites.append(LeelanauNews(keywords))
        # self.websites.append(HoughtonLakeResorter(keywords))
        # self.websites.append(IronMountainDailyNews(keywords))
        # self.websites.append(MiningJournal(keywords))
        # self.websites.append(TheAlpenaNews(keywords))

        # TODO: not working
        # self.websites.append(LakeOrionReview(keywords))
        # self.websites.append(ClarkstonNews(keywords))

        self.generateArticleCount()

    def generateArticleCount(self):
        for site in self.websites:
            self.articleCount = self.articleCount + site.getArticleCount()

    def getUrls(self):
        urls = []
        for site in self.websites:
            for url in site.getArticleLinks():
                urls.append(url)
            self.articleCount = self.articleCount + site.getArticleCount()
        return urls

    def getScrapedArticles(self):
        articles = []
        for site in self.websites:
            for article in site.getScrapedArticles():
                articles.append(article)
        return articles

    def addValidArticles(self, article):
        self.validArticles.append(article)

    def setValidArticles(self, articles):
        self.validArticles = articles

    def getValidArticles(self):
        return self.validArticles

    def storeInArticlesCollection(self, article):
        try:
            database.Articles(
                url=article['url'],
                title=article['title'],
                publishingDate=article['publishingDate']
            ).save()
        except:
            print("Unexpected error:", sys.exc_info()[0])
            # raise
            pass

    def getArticleCount(self):
        return self.articleCount

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
            print("Unexpected error:", sys.exc_info()[0])
            # raise
            pass

