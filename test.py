import requests
from bs4 import BeautifulSoup as soup
import newspaper
from validator_collection import validators, checkers
import re
from tqdm import tqdm
import time
from colorama import Fore
from newspaper import urls as urlChecker

websites = []

websites.append("https://www.ourmidland.com/news/article/UPDATE-Pine-River-spill-determined-to-be-15086305.php")
websites.append("https://www.ourmidland.com/news/article/City-Oil-slick-on-Pine-River-15084185.php")
websites.append("https://www.ourmidland.com/news/article/Clean-up-efforts-continue-on-Bush-Creek-15089825.php")
websites.append("https://www.ourmidland.com/news/article/Virginia-issues-violation-notice-to-Dominion-for-6906076.php")
websites.append("https://www.ourmidland.com/news/article/Tanker-rolls-on-Homer-Adams-15098387.php")
websites.append("https://thecountypress.mihomepaper.com/articles/deputy-director-at-msp-announces-jan-27-retirement/")
websites.append("https://www.lakecountystar.com/news/article/Official-Pine-River-spill-nbsp-is-dielectric-15086338.php")
websites.append("https://www.lakecountystar.com/news/article/UPDATE-Pine-River-spill-determined-to-be-15086305.php")
websites.append("https://www.lakecountystar.com/business/energy/article/Decades-after-oil-spill-Barnett-Shale-lake-15073316.php")
websites.append("https://www.lakecountystar.com/news/article/45-000-gallons-of-raw-sewage-spills-near-creek-15070289.php")
websites.append("https://www.lakecountystar.com/news/article/Semi-crashes-in-Montana-river-spilling-diesel-15067701.php")
websites.append("https://www.lakecountystar.com/news/article/Highway-22-closed-after-tanker-crash-diesel-spill-15063079.php")
websites.append("https://www.lakecountystar.com/news/medical/article/211M-gallons-of-sewage-spilled-into-Florida-city-15061667.php")
websites.append("https://www.northernexpress.com/news/opinion/the-audacity-of-enbridge/")
websites.append("https://www.manisteenews.com/editorials/article/Time-to-protect-Great-Lakes-from-oil-spill-is-now-14221909.php")
websites.append("https://www.manisteenews.com/state-news/article/Report-slams-Enbridge-Energy-s-history-of-oil-14228360.php")
websites.append("https://www.manisteenews.com/news/article/Official-Pine-River-spill-nbsp-is-dielectric-15086338.php")
websites.append("https://www.manisteenews.com/news/article/UPDATE-Pine-River-spill-determined-to-be-15086305.php")
websites.append("https://www.leelanaunews.com/articles/chemical-scare-in-elmwood-leads-to-evacuations/")
websites.append("https://www.ironmountaindailynews.com/news/local-news/2019/07/sewage-spills-into-escanaba-river/")
websites.append("https://www.miningjournal.net/news/michigan-news-apwire/2019/12/some-metals-not-found-in-river-spill/")
websites.append("https://www.miningjournal.net/news/michigan-news-apwire/2019/12/radiation-levels-ok-at-river-spill/")
websites.append("https://www.miningjournal.net/news/front-page-news/2018/07/report-lake-oil-spill-in-michigan-would-cost-nearly-2b/")
websites.append("https://www.miningjournal.net/news/2018/03/repairs-cleanup-completed-after-krist-oil-co-gas-station-fuel-spill/")
websites.append("https://www.thealpenanews.com/news/michigan-news-apwire/2020/01/epa-lead-uranium-found-after-detroit-river-spill/")
websites.append("https://www.thealpenanews.com/news/local-news/2019/07/gas-spill-in-the-thunder-bay-river/")
websites.append("https://www.thealpenanews.com/news/national-news-apwire/2017/09/evidence-of-spills-at-toxic-site-during-floods/")

for site in websites:
	print(site)



