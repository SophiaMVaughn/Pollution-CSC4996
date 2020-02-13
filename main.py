from newsWebsite import NewsWebsite
from crawler import Crawler
from scraper import Scraper

stignacenews = NewsWebsite("https://www.stignacenews.com", "title", "", "", "/articles/", False)
# crawler = Crawler(stignacenews, "pollution", "contamination")
#
# for url in crawler.getCrawledURLs():
#     print(url)

ourmidland = NewsWebsite("https://www.ourmidland.com", "title", "meta", "time", "/news/article/", False)
# crawler = Crawler(ourmidland, "pollution", "contamination")
#
# for url in crawler.getCrawledURLs():
#     print(url)

websiteList = [stignacenews,ourmidland]

scraper1 = Scraper("https://www.ourmidland.com/news/article/Environmentalists-challenge-DNR-sand-mine-8373534.php", websiteList)
