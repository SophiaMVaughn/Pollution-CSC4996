
from freepCrawler import FreepCrawler
from freepScraper import FreepScraper
import parse
import mongoengine

keyword = "spill"
crawler = FreepCrawler(keyword)
crawler.crawlURLs()

scrapedArticles = []
crawlCount = 0

db = mongoengine.connect(db="Pollution")
db.drop_database('Pollution')

for url in crawler.getURLs():
    article = FreepScraper(url)
    scrapedArticles.append(article)
    crawlCount = crawlCount + 1

print("\n[+] Crawled "+str(crawlCount)+" articles.\n")
print("[+] NLP analysis starting...")
print("============================\n")
print("Confirmed events")
print("----------------")

file=open("output.txt","a+")
file.write("------"+keyword+"---------------------------------------------\n")

eventCount = 0
filteredArticles = []

for article in scrapedArticles:
    if parse.isArticleEvent(article):
        file.write(article.getArticleTitle()+"\n")
        filteredArticles.append(article)
        eventCount = eventCount + 1
        print("[+] " + str(article.getArticleTitle()))

print("\n[+] NLP processing complete - confirmed " + str(eventCount) + " articles as contamination events\n")
print("[+] Populating database...")

for article in filteredArticles:
    article.storeInDatabase()

file.close()



