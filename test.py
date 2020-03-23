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
from newspaper import urls as urlChecker
from newspaper import Article
from dateutil import parser

website = Website("https://www.freep.com/")
website.searchForKey("pollution")
page = website.getCurrentPage()
links = page.find_all("a", href=True)

website.nextPage()
page = website.getCurrentPage()
links = links + page.find_all("a", href=True)

print(len(links))

print(len(links))
for link in links:
    print(link['href'])


