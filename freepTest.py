
from freepCrawler import FreepCrawler

crawler = FreepCrawler("pollution", "contamination")
crawler.crawlURLs()
crawler.scrapeURLs()

print("Article Titles")
print("---------------------------------------------------")

for article in crawler.getScrapedArticles():
    print(article.getArticleTitle())

