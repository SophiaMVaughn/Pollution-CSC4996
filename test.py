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

website = Website("https://www.record-eagle.com/")
website.searchForKey("pollution")

driver = website.getDriver()

articles = driver.find_elements_by_class_name("gs-title")
for article in articles:
    print(article)
    try:
        link = article.find_element_by_css_selector('a').get_attribute('href')
        print(link)
    except:
        pass