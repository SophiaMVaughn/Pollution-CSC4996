
from freepCrawler import FreepCrawler
from freepScraper import FreepScraper

crawler = FreepCrawler("pollution", "contamination")
crawler.crawlURLs()

scrapedArticles = []
crawlCount = 0

for url in crawler.getURLs():
    print("scraping " + str(url))
    article = FreepScraper(url)
    scrapedArticles.append(article)
    crawlCount = crawlCount + 1

print("\n[+] Crawled " + str(crawlCount) + " articles\n")
print("Article Titles")
print("---------------------------------------------------")

for article in scrapedArticles:
    print(article.getArticleTitle())


