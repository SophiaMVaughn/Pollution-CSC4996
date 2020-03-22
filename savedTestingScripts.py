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

websites = [
    "https://www.ourmidland.com/",
    "https://thecountypress.mihomepaper.com/",
    "https://www.lakecountystar.com/",
    "https://www.northernexpress.com/",
    "https://www.manisteenews.com/",
    "https://michiganchronicle.com/",
    "https://www.harborlightnews.com/",
    "https://thedailynews.cc/",
    "https://www.leelanaunews.com/",
    "https://www.houghtonlakeresorter.com/",
    "https://www.ironmountaindailynews.com/",
    "https://www.miningjournal.net/",
    "https://www.thealpenanews.com/",
    "http://www.marion-press.com/",
    "https://www.candgnews.com/",
    "https://www.mlive.com/",
    "https://www.leaderpub.com/",
    "https://www.record-eagle.com/",
    "https://www.macombdaily.com/",
    "https://www.theoaklandpress.com/",
    "https://www.shorelinemedia.net/",
    "https://clarkstonnews.com/",
    "https://lakeorionreview.com/",
    "https://www.detroitnews.com/",
    "https://www.freep.com/",
    "https://www.thetimesherald.com/"
]

for website in websites:
    links = newspaper.build(website, memoize_articles=False)
    print(website + " --> " + str(len(links.articles)))

#########################################################################