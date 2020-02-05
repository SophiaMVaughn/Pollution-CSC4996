from crawler import NewsWebsite
from crawler import Crawler

links = open("resources/testURLs.txt", "r").readlines()

urls = []

for link in links:
    urls.append(link.strip())

websiteObjects = []

websiteObjects.append(NewsWebsite(urls[0], "lenconnect", "headline", "", "", "", "/search?text=", False))

crawler = Crawler(websiteObjects, "Pollution")