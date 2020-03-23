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
from newspaper import Article
from dateutil import parser

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

urls = [
    "https://www.candgnews.com/news/noise-pollution-health-issue-84629",
    "https://www.mlive.com/news/2019/08/is-it-pollution-drone-photos-trigger-lake-michigan-beach-worries.html",
    "https://www.leaderpub.com/2019/02/14/parrish-the-dark-side-of-light-pollution/",
    "http://www.marion-press.com/?s=pollution&x=0&y=0",
    "https://thecountypress.mihomepaper.com/articles/howell-bill-improves-technical-error-in-2018-solid-waste-statute/",
    "https://www.lakecountystar.com/news/science/article/As-virus-shuts-down-cities-in-Europe-pollution-15136712.php",
    "https://www.record-eagle.com/nation_world/coronavirus-rekindles-oil-spill-memories-along-gulf-coast/image_17364979-9ec8-5ae9-9e1e-676c6981beba.html",
    "https://www.macombdaily.com/online_features/green_living/are-your-recyclable-products-actually-recyclable/article_6f2fd507-de12-5a51-b76e-b8feb2e5721b.html",
    "https://www.northernexpress.com/news/feature/get-your-zen-on/",
    "https://www.manisteenews.com/state-news/article/Michigan-Sugar-Company-settles-air-water-14245207.php",
    "https://www.theoaklandpress.com/lifestyles/health/do-masks-offer-protection-from-new-virus-it-depends/article_586a5060-445c-11ea-8319-cf088ed7e72a.html",
    "https://michiganchronicle.com/2013/07/03/new-nrdc-climate-analysis-nation-can-create-jobs-and-save-on-electricity-bills-while-cutting-carbon-pollution-from-power-plants/",
    "https://clarkstonnews.com/cleaning-up-the-beach-to-serve-the-community/",
    "https://www.harborlightnews.com/articles/a-home-with-a-view/",
    "https://thedailynews.cc/articles/federal-mogul-works-to-fix-pollution-problems/",
    "https://lakeorionreview.com/lake-orion-high-school-science-students-clean-up-along-paint-creek/",
    "https://www.leelanaunews.com/articles/bata-cuts-county-route/",
    "https://www.houghtonlakeresorter.com/articles/former-rhs-student-imparts-overseas-experiences-as-ibm-employee/",
    "https://www.detroitnews.com/story/news/local/michigan/2020/02/14/ohio-lake-erie-pollution-diet/111320920/",
    "https://www.freep.com/story/news/local/michigan/2020/02/13/ohio-wants-put-lake-erie-new-strict-pollution-diet/4754710002/",
    "https://www.thetimesherald.com/story/news/2020/02/28/whats-chirping-sound-mdnr-needs-help-frog-toad-survey/4859228002/",
    "https://www.ironmountaindailynews.com/news/local-news/2020/02/grants-seek-market-based-reductions-of-lakes-pollution/",
    "https://www.miningjournal.net/news/front-page-news/2019/06/johnson-controls-accused-of-failing-to-report-pollution/",
    "https://www.thealpenanews.com/news/national-news-apwire/2020/02/scientists-gather-to-study-the-risk-from-microplastic-pollution/"
]

i = "hello"
si = str(i)
for url in urls:
    article = Article(url)
    article.download()
    article.parse()
    if article.publish_date is not None:
        d = parser.parse(str(article.publish_date))
        print(d.strftime("%m/%d/%Y"))

