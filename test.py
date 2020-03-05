import requests
from bs4 import BeautifulSoup as soup
import newspaper
from validator_collection import validators, checkers
import re
from tqdm import tqdm
import time
from colorama import Fore
from newspaper import urls as urlChecker
import json
from scraperInterface import ScraperInterface


baseUrl = "https://www.ourmidland.com/"
page = requests.get("https://www.ourmidland.com/search/?action=search&firstRequest=1&searchindex=solr&query=spill")
soup_page = soup(page.content, 'html.parser')
urls_list = soup_page.find_all("a", href=True)
urls = []

for url in urls_list:
    urls.append(url['href'])

def filterLinksForArticles(urls):
    validArticleUrls = []
    for url in urls:
        if "http" not in url:
            url = baseUrl + url
        urlSplit = url.split("/")
        if len(urlSplit) < 5:
            continue
        if urlSplit[-2:-1][0].isnumeric() and urlSplit[-3:-2][0].isnumeric():
            continue
        if urlChecker.valid_url(url):
            validArticleUrls.append(url)
    return validArticleUrls

for url in filterLinksForArticles(urls):
    pass

url = "https://www.ourmidland.com//news/article/Work-crews-returning-to-site-of-massive-Colorado-8373790.php"
print(urlChecker.valid_url(url))