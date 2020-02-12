from crawler import NewsWebsite
from crawler import Crawler

newsWebsite = NewsWebsite("https://www.stignacenews.com/", "", "", "", "", "https://www.stignacenews.com/articles", False)
crawler = Crawler(newsWebsite, "pollution", "contamination")
for url in crawler.getCrawledURLs():
    print(url)

