from newsWebsite import NewsWebsite
from crawler import Crawler
from scraper import Scraper

stignacenewsSearchStructure = "https://www.stignacenews.com/page/PEATPAGE/?s=PEATKEY"
ourmidlandSearchStructure = "https://www.ourmidland.com/search/?action=search&searchindex=solr&query=PEATKEY&page=PEATPAGE"
michigansthumbSearchStructure = "https://www.michigansthumb.com/search/?action=search&searchindex=solr&query=PEATKEY&page=PEATPAGE"

# create NewsWebsite objects
stignacenews = NewsWebsite("https://www.stignacenews.com", "title", "", "", stignacenewsSearchStructure, "/articles/", False)
ourmidland = NewsWebsite("https://www.ourmidland.com", "title", "p", "time", "/news/article/", ourmidlandSearchStructure, False)
michigansthumb = NewsWebsite("https://www.michigansthumb.com/", "title", "p", "time", michigansthumbSearchStructure, "/news/article", False)

# crate Crawler objects
crawler = Crawler(michigansthumb, "pollution", "contamination")

websiteList = [stignacenews,ourmidland,michigansthumb]

# create Scraper objects
scraper = Scraper("https://www.ourmidland.com/news/article/SVSU-receives-nbsp-grant-aimed-at-nbsp-watershed-13319728.php", websiteList)
