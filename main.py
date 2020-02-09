from crawler import NewsWebsite
from crawler import Crawler

newsWebsite = NewsWebsite("https://www.stignacenews.com/", "", "", "", "", "oht-article", False)
crawler = Crawler(newsWebsite, "pollution")
