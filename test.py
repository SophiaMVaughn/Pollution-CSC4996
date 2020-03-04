import requests
from bs4 import BeautifulSoup as soup
import newspaper
from validator_collection import validators, checkers
import re
from tqdm import tqdm
import time
from colorama import Fore
from newspaper import urls as urlChecker

def filterLinksForArticles(urls):
    validArticleUrls = []
    for url in urls:
        if "http" not in url:
            url = "https://www.lakecountystar.com/" + url
        urlSplit = url.split("/")
        print(url)
        if len(urlSplit) < 5:
            continue
        if urlSplit[-2:-1][0].isnumeric() and urlSplit[-3:-2][0].isnumeric():
            continue
        if urlChecker.valid_url(url):
            validArticleUrls.append(url)
    return validArticleUrls


urls = [
    "/local-news/article/Yet-another-downside-to-big-snow-pollution-14388589.php",
    "/news/article/International-company-settles-EPA-water-pollution-15092454.php"
]

url = "https://www.lakecountystar.com/search/?action=search&searchindex=solr&query=pollution&page=1"

print(urlChecker.valid_url(url))





