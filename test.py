import requests
from bs4 import BeautifulSoup as soup
import newspaper
from newspaper import urls
from validator_collection import validators, checkers
import re

url = "http://www.marion-press.com/2020/03/dont-tell-these-seniors-they-are-too-old-to-party/"
page = requests.get(url)
soupPage = soup(page.content, 'html.parser')
bodyList = soupPage.find_all("p")

body = ""
for lines in bodyList:
    body = body + " " + lines.get_text()
    newBody = re.sub("\s\s+", " ", body)

print(newBody)
