from newsWebsite import NewsWebsite
from crawler import Crawler
from scraper import Scraper

stignacenews = NewsWebsite("https://www.stignacenews.com", "title", "", "",
                           "https://www.stignacenews.com/page/PEATPAGE/?s=PEATKEY", "/articles/", False)

print(stignacenews.getSearchQuery("pollution", 3))

