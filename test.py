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
import sys
import datetime
from selenium import webdriver
from sys import platform
from selenium.webdriver.chrome.options import Options
import os
from website import Website
from crawler import Crawler
from scraper import Scraper
from newspaper import urls as urlChecker
from newspaper import Article
from dateutil import parser

# keywords = ['pollution']
# crawler = Crawler("https://lakeorionreview.com/", keywords)
#
# for article in crawler.getArticleLinks():
#     print("Scraping  " + str(article))
#     try:
#         scraper = Scraper(article)
#     except:
#         print("  Could not connect to " + str(article))

def test():
    return 1/0

try:
    test = test()
except:
    print("Can't divide by 0")

