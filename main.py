from newsWebsite import NewsWebsite
from crawler import Crawler
from scraper import Scraper

# create NewsWebsite objects
stignacenews = NewsWebsite("https://www.stignacenews.com", "title", "", "", "/articles/", False)
ourmidland = NewsWebsite("https://www.ourmidland.com", "title", "p", "time", "/news/article/", False)
michigansthumb = NewsWebsite("https://www.michigansthumb.com/", "title", "p", "time", "/news/article", False)

# crate Crawler objects
crawler = Crawler(michigansthumb, "pollution", "contamination")

websiteList = [stignacenews,ourmidland,michigansthumb]

# create Scraper objects
scraper = Scraper("https://www.ourmidland.com/news/article/SVSU-receives-nbsp-grant-aimed-at-nbsp-watershed-13319728.php", websiteList)

print("\ntitle")
print("#################################")
print(scraper.getArticleTitle())

print("\ndate")
print("#################################")
print(scraper.getArticleDate())

print("\nbody")
print("#################################")
body = scraper.getArticleBody()
for line in body:
    print(line)
