from scraper import Scraper
import sys

# Not yet implemented
# ----------------------------
# https://www.candgnews.com/
# https://www.mlive.com/
# https://www.leaderpub.com/
# https://www.macombdaily.com/
# https://www.theoaklandpress.com/
# https://www.shorelinemedia.net/
# https://www.detroitnews.com/
# https://www.freep.com/
# https://www.thetimesherald.com/


class Ourmidland(Scraper):
    def __init__(self, keywords):
        super().__init__()
        self.setKeywords(keywords)
        self.setBaseUrl("https://www.ourmidland.com/")
        self.setSearchQueryStructure("https://www.ourmidland.com/search/?action=search&searchindex=solr&query=PEATKEY&page=PEATPAGE")
        try:
            self.crawl()
        except:
            print("[-] Error crawling marion-press.com:", sys.exc_info()[0])
            raise
        self.scrapeAll()

    def filterLinksForArticles(self, links):
        filteredLinks = []
        for link in links:
            if "/article/" in link:
                link = "https://www.ourmidland.com" + link
                filteredLinks.append(link)
        return filteredLinks


class MarionPress(Scraper):
    def __init__(self, keywords):
        super().__init__()
        self.setKeywords(keywords)
        self.setBaseUrl("http://www.marion-press.com/")
        self.setSearchQueryStructure("http://www.marion-press.com/page/PEATPAGE/?s=PEATKEY&x=0&y=0")
        try:
            self.crawl()
        except:
            print("[-] Error crawling marion-press.com:", sys.exc_info()[0])
            raise
        self.scrapeAll()


class TheCountyPress(Scraper):
    def __init__(self, keywords):
        super().__init__()
        self.setKeywords(keywords)
        self.setBaseUrl("https://thecountypress.mihomepaper.com/")
        self.setSearchQueryStructure("https://thecountypress.mihomepaper.com/page/PEATPAGE/?s=PEATKEY")
        try:
            self.crawl()
        except:
            print("[-] Error crawling thecountypress.mihomepaper.com:", sys.exc_info()[0])
            raise
        self.scrapeAll()


class LakeCountyStar(Scraper):
    def __init__(self, keywords):
        super().__init__()
        self.setKeywords(keywords)
        self.setBaseUrl("https://www.lakecountystar.com/")
        self.setSearchQueryStructure("https://www.lakecountystar.com/search/?action=search&searchindex=solr&query=PEATKEY&page=PEATPAGE")
        try:
            self.crawl()
        except:
            print("[-] Error crawling lakecountystar.com:", sys.exc_info()[0])
            raise
        self.scrapeAll()

    def filterLinksForArticles(self, links):
        filteredLinks = []
        for link in links:
            if "/article/" in link:
                link = "https://www.lakecountystar.com" + link
                filteredLinks.append(link)
        return filteredLinks


class NorthernExpress(Scraper):
    def __init__(self, keywords):
        super().__init__()
        self.setKeywords(keywords)
        self.setBaseUrl("https://www.northernexpress.com/")
        self.setSearchQueryStructure("https://www.northernexpress.com/search/?query=PEATKEY&content=news&page=PEATPAGE")
        try:
            self.crawl()
        except:
            print("[-] Error crawling northernexpress.com:", sys.exc_info()[0])
            raise
        self.scrapeAll()

    def filterLinksForArticles(self, links):
        filteredLinks = []
        for link in links:
            if "/news/" in link:
                linkSplit = link.split("/")
                if len(linkSplit) > 4:
                    link = "https://www.northernexpress.com" + link
                    filteredLinks.append(link)
        return filteredLinks


class ManisteeNews(Scraper):
    def __init__(self, keywords):
        super().__init__()
        self.setKeywords(keywords)
        self.setBaseUrl("https://www.manisteenews.com/")
        self.setSearchQueryStructure("https://www.manisteenews.com/search/?action=search&searchindex=solr&query=PEATKEY&page=PEATPAGE")
        try:
            self.crawl()
        except:
            print("[-] Error crawling manisteenews.com:", sys.exc_info()[0])
            raise
        self.scrapeAll()

    def filterLinksForArticles(self, links):
        filteredLinks = []
        for link in links:
            if "/article/" in link:
                link = "https://www.manisteenews.com" + link
                filteredLinks.append(link)
        return filteredLinks


# TODO: not scraping links
class MichiganChronicle(Scraper):
    def __init__(self, keywords):
        super().__init__()
        self.setKeywords(keywords)
        self.setBaseUrl("https://michiganchronicle.com/")
        self.setSearchQueryStructure("https://michiganchronicle.com/page/PEATPAGE/?s=PEATKEY")
        try:
            self.crawl()
        except:
            print("[-] Error crawling michiganchronicle.com:", sys.exc_info()[0])
            raise
        self.scrapeAll()


class ClarkstonNews(Scraper):
    def __init__(self, keywords):
        super().__init__()
        self.setKeywords(keywords)
        self.setBaseUrl("https://clarkstonnews.com/")
        self.setSearchQueryStructure("https://clarkstonnews.com/page/PEATPAGE/?s=PEATKEY")
        try:
            self.crawl()
        except:
            print("[-] Error crawling clarkstonnews.com:", sys.exc_info()[0])
            raise
        self.scrapeAll()


class HarborLightNews(Scraper):
    def __init__(self, keywords):
        super().__init__()
        self.setKeywords(keywords)
        self.setBaseUrl("https://www.harborlightnews.com/")
        self.setSearchQueryStructure("https://www.harborlightnews.com/page/PEATPAGE/?s=PEATKEY")
        try:
            self.crawl()
        except:
            print("[-] Error crawling harborlightnews.com:", sys.exc_info()[0])
            raise
        self.scrapeAll()


class TheDailyNews(Scraper):
    def __init__(self, keywords):
        super().__init__()
        self.setKeywords(keywords)
        self.setBaseUrl("https://thedailynews.cc/")
        self.setSearchQueryStructure("https://thedailynews.cc/page/PEATPAGE/?s=PEATKEY")
        try:
            self.crawl()
        except:
            print("[-] Error crawling thedailynews.cc:", sys.exc_info()[0])
            raise
        self.scrapeAll()


# TODO: not working
class LakeOrionReview(Scraper):
    def __init__(self, keywords):
        super().__init__()
        self.setKeywords(keywords)
        self.setBaseUrl("https://lakeorionreview.com/")
        self.setSearchQueryStructure("https://lakeorionreview.com/page/PEATPAGE/?s=PEATKEY")
        try:
            self.crawl()
        except:
            print("[-] Error crawling lakeorionreview.com:", sys.exc_info()[0])
            raise
        self.scrapeAll()


class LeelanauNews(Scraper):
    def __init__(self, keywords):
        super().__init__()
        self.setKeywords(keywords)
        self.setBaseUrl("https://www.leelanaunews.com/")
        self.setSearchQueryStructure("https://www.leelanaunews.com/page/PEATPAGE/?s=PEATKEY")
        try:
            self.crawl()
        except:
            print("[-] Error crawling leelanaunews.com:", sys.exc_info()[0])
            raise
        self.scrapeAll()


class HoughtonLakeResorter(Scraper):
    def __init__(self, keywords):
        super().__init__()
        self.setKeywords(keywords)
        self.setBaseUrl("https://www.houghtonlakeresorter.com/")
        self.setSearchQueryStructure("https://www.houghtonlakeresorter.com/page/PEATPAGE/?s=PEATKEY")
        try:
            self.crawl()
        except:
            print("[-] Error crawling houghtonlakeresorter.com:", sys.exc_info()[0])
            raise


class IronMountainDailyNews(Scraper):
    def __init__(self, keywords):
        super().__init__()
        self.setKeywords(keywords)
        self.setBaseUrl("https://www.ironmountaindailynews.com/")
        self.setSearchQueryStructure("https://www.ironmountaindailynews.com/search/PEATKEY/page/PEATPAGE/")
        try:
            self.crawl()
        except:
            print("[-] Error crawling ironmountaindailynews.com:", sys.exc_info()[0])
            raise
        self.scrapeAll()


class MiningJournal(Scraper):
    def __init__(self, keywords):
        super().__init__()
        self.setKeywords(keywords)
        self.setBaseUrl("https://www.miningjournal.net/")
        self.setSearchQueryStructure("https://www.miningjournal.net/search/PEATKEY/page/PEATPAGE/")
        try:
            self.crawl()
        except:
            print("[-] Error crawling miningjournal.net:", sys.exc_info()[0])
            raise
        self.scrapeAll()


class TheAlpenaNews(Scraper):
    def __init__(self, keywords):
        super().__init__()
        self.setKeywords(keywords)
        self.setBaseUrl("https://www.thealpenanews.com/")
        self.setSearchQueryStructure("https://www.thealpenanews.com/search/PEATKEY/page/PEATPAGE/")
        try:
            self.crawl()
        except:
            print("[-] Error crawling thealpenanews.com:", sys.exc_info()[0])
            raise
        self.scrapeAll()

