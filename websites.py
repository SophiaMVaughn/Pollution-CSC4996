from scraper import Scraper

class Ourmidland(Scraper):
    def __init__(self, keywords):
        super().__init__()
        self.setKeywords(keywords)
        self.setBaseUrl("https://www.ourmidland.com/")
        self.setSearchQueryStructure("https://www.ourmidland.com/search/?action=search&searchindex=solr&query=PEATKEY&page=PEATPAGE")
        self.crawl()
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
        self.crawl()
        self.scrapeAll()

    def filterLinksForArticles(self, links):
        filteredLinks = []
        for link in links:
            linkSplit = link.split("/")
            if len(linkSplit) > 6:
                if linkSplit[3].isnumeric() and linkSplit[4].isnumeric():
                    filteredLinks.append(link)
        return filteredLinks


class TheCountyPress(Scraper):
    def __init__(self, keywords):
        super().__init__()
        self.setKeywords(keywords)
        self.setBaseUrl("https://thecountypress.mihomepaper.com/")
        self.setSearchQueryStructure("https://thecountypress.mihomepaper.com/page/PEATPAGE/?s=PEATKEY")
        self.crawl()
        self.scrapeAll()

    def filterLinksForArticles(self, links):
        filteredLinks = []
        for link in links:
            if "/articles/" in link:
                filteredLinks.append(link)
        return filteredLinks


class LakeCountyStar(Scraper):
    def __init__(self, keywords):
        super().__init__()
        self.setKeywords(keywords)
        self.setBaseUrl("https://www.lakecountystar.com/")
        self.setSearchQueryStructure("https://www.lakecountystar.com/search/?action=search&searchindex=solr&query=PEATKEY&page=PEATPAGE")
        self.crawl()
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
        self.crawl()
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
        self.crawl()
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
        self.crawl()
        self.scrapeAll()


class ClarkstonNews(Scraper):
    def __init__(self, keywords):
        super().__init__()
        self.setKeywords(keywords)
        self.setBaseUrl("https://clarkstonnews.com/")
        self.setSearchQueryStructure("https://clarkstonnews.com/page/PEATPAGE/?s=PEATKEY")
        self.crawl()
        self.scrapeAll()

    # TODO: not the best way to scrape articles
    def filterLinksForArticles(self, links):
        filteredLinks = []
        for link in links:
            linkSplit = link.split("/")
            if len(linkSplit) > 5:
                filteredLinks.append(link)
        return filteredLinks


class HarborLightNews(Scraper):
    def __init__(self, keywords):
        super().__init__()
        self.setKeywords(keywords)
        self.setBaseUrl("https://www.harborlightnews.com/")
        self.setSearchQueryStructure("https://www.harborlightnews.com/page/PEATPAGE/?s=PEATKEY")
        self.crawl()
        self.scrapeAll()

    def filterLinksForArticles(self, links):
        filteredLinks = []
        for link in links:
            if "/articles/" in link:
                filteredLinks.append(link)
        return filteredLinks


class TheDailyNews(Scraper):
    def __init__(self, keywords):
        super().__init__()
        self.setKeywords(keywords)
        self.setBaseUrl("https://thedailynews.cc/")
        self.setSearchQueryStructure("https://thedailynews.cc/page/PEATPAGE/?s=PEATKEY")
        self.crawl()
        self.scrapeAll()

    def filterLinksForArticles(self, links):
        filteredLinks = []
        for link in links:
            if "/articles/" in link:
                filteredLinks.append(link)
        return filteredLinks


# TODO: not working
class LakeOrionReview(Scraper):
    def __init__(self, keywords):
        super().__init__()
        self.setKeywords(keywords)
        self.setBaseUrl("https://lakeorionreview.com/")
        self.setSearchQueryStructure("https://lakeorionreview.com/page/PEATPAGE/?s=PEATKEY")
        self.crawl()
        self.scrapeAll()


class LeelanauNews(Scraper):
    def __init__(self, keywords):
        super().__init__()
        self.setKeywords(keywords)
        self.setBaseUrl("https://www.leelanaunews.com/")
        self.setSearchQueryStructure("https://www.leelanaunews.com/page/PEATPAGE/?s=PEATKEY")
        self.crawl()
        self.scrapeAll()

    def filterLinksForArticles(self, links):
        filteredLinks = []
        for link in links:
            if "/articles/" in link:
                filteredLinks.append(link)
        return filteredLinks


class HoughtonLakeResorter(Scraper):
    def __init__(self, keywords):
        super().__init__()
        self.setKeywords(keywords)
        self.setBaseUrl("https://www.houghtonlakeresorter.com/")
        self.setSearchQueryStructure("https://www.houghtonlakeresorter.com/page/PEATPAGE/?s=PEATKEY")
        self.crawl()
        self.scrapeAll()

    def filterLinksForArticles(self, links):
        filteredLinks = []
        for link in links:
            if "/articles/" in link:
                filteredLinks.append(link)
        return filteredLinks


class IronMountainDailyNews(Scraper):
    def __init__(self, keywords):
        super().__init__()
        self.setKeywords(keywords)
        self.setBaseUrl("https://www.ironmountaindailynews.com/")
        self.setSearchQueryStructure("https://www.ironmountaindailynews.com/search/PEATKEY/page/PEATPAGE/")
        self.crawl()
        self.scrapeAll()

    def filterLinksForArticles(self, links):
        filteredLinks = []
        for link in links:
            linkSplit = link.split("/")
            if len(linkSplit) > 5:
                if linkSplit[-3].isnumeric() and linkSplit[-4].isnumeric():
                    filteredLinks.append(link)
        return filteredLinks


class MiningJournal(Scraper):
    def __init__(self, keywords):
        super().__init__()
        self.setKeywords(keywords)
        self.setBaseUrl("https://www.miningjournal.net/")
        self.setSearchQueryStructure("https://www.miningjournal.net/search/PEATKEY/page/PEATPAGE/")
        self.crawl()
        self.scrapeAll()

    def filterLinksForArticles(self, links):
        filteredLinks = []
        for link in links:
            linkSplit = link.split("/")
            if len(linkSplit) > 5:
                if linkSplit[-3].isnumeric() and linkSplit[-4].isnumeric():
                    filteredLinks.append(link)
        return filteredLinks


class TheAlpenaNews(Scraper):
    def __init__(self, keywords):
        super().__init__()
        self.setKeywords(keywords)
        self.setBaseUrl("https://www.thealpenanews.com/")
        self.setSearchQueryStructure("https://www.thealpenanews.com/search/PEATKEY/page/PEATPAGE/")
        self.crawl()
        self.scrapeAll()

    def filterLinksForArticles(self, links):
        filteredLinks = []
        for link in links:
            linkSplit = link.split("/")
            if len(linkSplit) > 5:
                if linkSplit[-3].isnumeric() and linkSplit[-4].isnumeric():
                    filteredLinks.append(link)
        return filteredLinks