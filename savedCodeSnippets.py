import requests
from bs4 import BeautifulSoup as soup
from newspaper import urls
from validator_collection import validators, checkers

##########################################################################################

page = requests.get("http://www.marion-press.com/?s=pollution&x=0&y=0")
soupPage = soup(page.content,'html.parser')
links = soupPage.find_all('a', href=True)

count = 0
for url in links:
    url = url['href']
    if checkers.is_url(url):
        count = count + 1
        print(url)

print(str(count) + " of " + str(len(links)) + " links are articles")

##########################################################################################

page = requests.get("http://www.marion-press.com/2020/01/asian-rivers-riddled-with-plastic-trash/")
soupPage = soup(page.content,'html.parser')
links = soupPage.find_all('a', href=True)

count = 0
for url in links:
    url = url['href']
    urlSplit = url.split("/")
    if len(urlSplit) < 5:
        continue
    if urlSplit[-2:-1][0].isnumeric() and urlSplit[-3:-2][0].isnumeric():
        continue
    if urls.valid_url(url):
        print(url)
        count = count + 1

print(str(count) + " of " + str(len(links)) + " links are articles")

##########################################################################################
