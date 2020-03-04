import requests
from bs4 import BeautifulSoup as soup
import database
import newspaper
from newspaper import urls as urlChecker
from textColors import bcolors


class Crawler:
    def __init__(self):
        self.baseUrl = ""
        self.keywords = []
        self.articleLinks = []
        self.homePageArticleLinks = []
        self.articleCount = 0

    def demoCrawl(self):

        links = []


        if self.baseUrl == "https://www.ourmidland.com/":
            links.append("https://www.ourmidland.com/news/article/UPDATE-Pine-River-spill-determined-to-be-15086305.php")
            links.append("https://www.ourmidland.com/news/article/City-Oil-slick-on-Pine-River-15084185.php")
            links.append("https://www.ourmidland.com/news/article/Clean-up-efforts-continue-on-Bush-Creek-15089825.php")
            links.append("https://www.ourmidland.com/news/article/Virginia-issues-violation-notice-to-Dominion-for-6906076.php")
            links.append("https://www.ourmidland.com/news/article/Tanker-rolls-on-Homer-Adams-15098387.php")

        elif self.baseUrl == "http://www.marion-press.com/":
            pass

        elif self.baseUrl == "https://thecountypress.mihomepaper.com/":
            links.append("https://thecountypress.mihomepaper.com/articles/deputy-director-at-msp-announces-jan-27-retirement/")

        elif self.baseUrl == "https://www.lakecountystar.com/":
            links.append("https://www.lakecountystar.com/news/article/Official-Pine-River-spill-nbsp-is-dielectric-15086338.php")
            links.append("https://www.lakecountystar.com/news/article/UPDATE-Pine-River-spill-determined-to-be-15086305.php")
            links.append("https://www.lakecountystar.com/business/energy/article/Decades-after-oil-spill-Barnett-Shale-lake-15073316.php")
            links.append("https://www.lakecountystar.com/news/article/45-000-gallons-of-raw-sewage-spills-near-creek-15070289.php")
            links.append("https://www.lakecountystar.com/news/article/Semi-crashes-in-Montana-river-spilling-diesel-15067701.php")
            links.append("https://www.lakecountystar.com/news/article/Highway-22-closed-after-tanker-crash-diesel-spill-15063079.php")
            links.append("https://www.lakecountystar.com/news/medical/article/211M-gallons-of-sewage-spilled-into-Florida-city-15061667.php")

        elif self.baseUrl == "https://www.northernexpress.com/":
            pass

        elif self.baseUrl == "https://www.manisteenews.com/":
            links.append("https://www.manisteenews.com/editorials/article/Time-to-protect-Great-Lakes-from-oil-spill-is-now-14221909.php")
            links.append("https://www.manisteenews.com/state-news/article/Report-slams-Enbridge-Energy-s-history-of-oil-14228360.php")
            links.append("https://www.manisteenews.com/news/article/Official-Pine-River-spill-nbsp-is-dielectric-15086338.php")
            links.append("https://www.manisteenews.com/news/article/UPDATE-Pine-River-spill-determined-to-be-15086305.php")

        elif self.baseUrl == "https://michiganchronicle.com/":
            pass

        elif self.baseUrl == "https://clarkstonnews.com/":
            pass

        elif self.baseUrl == "https://www.harborlightnews.com/":
            pass

        elif self.baseUrl == "https://thedailynews.cc/":
            pass
        
        elif self.baseUrl == "https://lakeorionreview.com/":
            pass

        elif self.baseUrl == "https://www.leelanaunews.com/":
            links.append("https://www.leelanaunews.com/articles/chemical-scare-in-elmwood-leads-to-evacuations/")

        elif self.baseUrl == "https://www.houghtonlakeresorter.com/":
            pass
        elif self.baseUrl == "https://www.ironmountaindailynews.com/":
            links.append("https://www.ironmountaindailynews.com/news/local-news/2019/07/sewage-spills-into-escanaba-river/")

        elif self.baseUrl == "https://www.miningjournal.net/":
            links.append("https://www.miningjournal.net/news/michigan-news-apwire/2019/12/some-metals-not-found-in-river-spill/")
            links.append("https://www.miningjournal.net/news/michigan-news-apwire/2019/12/radiation-levels-ok-at-river-spill/")
            links.append("https://www.miningjournal.net/news/front-page-news/2018/07/report-lake-oil-spill-in-michigan-would-cost-nearly-2b/")
            links.append("https://www.miningjournal.net/news/2018/03/repairs-cleanup-completed-after-krist-oil-co-gas-station-fuel-spill/")

        elif self.baseUrl == "https://www.thealpenanews.com/":
            links.append("https://www.thealpenanews.com/news/michigan-news-apwire/2020/01/epa-lead-uranium-found-after-detroit-river-spill/")
            links.append("https://www.thealpenanews.com/news/local-news/2019/07/gas-spill-in-the-thunder-bay-river/")
            links.append("https://www.thealpenanews.com/news/national-news-apwire/2017/09/evidence-of-spills-at-toxic-site-during-floods/")


        print("\r" + bcolors.OKGREEN + "[+]" + bcolors.ENDC + " Crawling " + self.baseUrl
              + ": " + bcolors.OKGREEN + str(len(self.articleLinks)) + " URLs retrieved" + bcolors.ENDC)

    def crawl(self):
        links = []
        for keyword in self.keywords:
            query = self.searchQuery.replace("PEATKEY", keyword).replace("PEATPAGE","1")

            page = requests.get(query)

            soupLinks = self.scrapeArticleLinks(page)

            for link in soupLinks:
                if link['href'] not in links:
                    links.append(link['href'])

        self.articleLinks = self.filterLinksForArticles(links)
        self.articleCount = self.articleCount + len(self.articleLinks)
        self.storeInUrlsCollection(self.articleLinks)

        # print("\r" + bcolors.OKGREEN + "[+]" + bcolors.ENDC + " Crawling " + self.baseUrl
        #       + " for keyword " + bcolors.WARNING + "\'%s\'" % (keyword) + bcolors.ENDC + ": " +
        #       bcolors.OKGREEN + str(len(self.articleLinks)) + " URLs retrieved" + bcolors.ENDC)

        print("\r" + bcolors.OKGREEN + "[+]" + bcolors.ENDC + " Crawling " + self.baseUrl
              + ": " + bcolors.OKGREEN + str(len(self.articleLinks)) + " URLs retrieved" + bcolors.ENDC)

    def crawlHomePage(self):
        links = newspaper.build(self.baseUrl, memoize_articles=False)
        for article in links.articles:
            self.homePageArticleLinks.append(article.url)
        self.storeInUrlsCollection(self.homePageArticleLinks)

    def filterLinksForArticles(self, urls):
        validArticleUrls = []
        for url in urls:
            if "http" not in url:
                url = self.baseUrl + url
            urlSplit = url.split("/")
            if len(urlSplit) < 5:
                continue
            if urlSplit[-2:-1][0].isnumeric() and urlSplit[-3:-2][0].isnumeric():
                continue
            if urlChecker.valid_url(url):
                validArticleUrls.append(url)
        return validArticleUrls

    def setBaseUrl(self, url):
        self.baseUrl = url

    def setKeywords(self, keywords):
        self.keywords = keywords

    def getKeywords(self):
        return self.keywords

    def setSearchQueryStructure(self, query):
        self.searchQuery = query

    def scrapeArticleLinks(self, page):
        # TODO: try overriding this in the website classes and use tree structure of search pages
        #  to get article urls
        soupPage = soup(page.content, "html.parser")
        return soupPage.find_all('a', href=True)

    def getArticleLinks(self):
        return self.articleLinks

    def getArticleCount(self):
        return self.articleCount

    def storeInUrlsCollection(self, urls):
        for url in urls:
            try:
                database.Urls(url=url).save()
            except:
                pass