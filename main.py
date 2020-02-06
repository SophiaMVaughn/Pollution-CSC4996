
from freepCrawler import FreepCrawler
from freepScraper import FreepScraper
import parse
import mongoengine

keyword = "pollution"
crawler = FreepCrawler(keyword)
crawler.crawlURLs()

scrapedArticles = []
crawlCount = 0

db = mongoengine.connect(db="Pollution")
db.drop_database('Pollution')

for url in crawler.getURLs():
    print("scraping " + str(url))
    article = FreepScraper(url)
    article.storeInDatabase()
    scrapedArticles.append(article)
    crawlCount = crawlCount + 1

file=open("output.txt","a+")
file.write("------"+keyword+"---------------------------------------------")

for article in scrapedArticles:
    if parse.isArticleEvent(article):
        file.write(article.getArticleTitle())
    


