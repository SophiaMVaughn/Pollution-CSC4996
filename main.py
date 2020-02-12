from newsWebsite import NewsWebsite
from crawler import Crawler
from scraper import Scraper

stignacenews = NewsWebsite("https://www.stignacenews.com", "", "", "", "/articles/", False)
# crawler = Crawler(stignacenews, "pollution", "contamination")
#
# for url in crawler.getCrawledURLs():
#     print(url)

ourmidland = NewsWebsite("https://www.ourmidland.com", "", "", "", "/news/article/", False)
# crawler = Crawler(ourmidland, "pollution", "contamination")
#
# for url in crawler.getCrawledURLs():
#     print(url)

websiteList = [stignacenews,ourmidland]

scraper = Scraper("https://www.stignacenews.com/articles/peters-named-among-most-effective-lawmakers/", websiteList)