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
# from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options
import os
from website import Website
from crawler import Crawler
from scraper import Scraper
from newspaper import urls as urlChecker
from newspaper import Article
from dateutil import parser
import traceback

class myException(Exception):
    def __init__(self, string):
        self.string = string
    def __str__(self):
        return "This is my exception: " + self.string

raise myException("hello")

