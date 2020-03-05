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

with open('websites.json') as data_file:
    websites = json.load(data_file)

for website, attributes in websites.items():
    print(website)