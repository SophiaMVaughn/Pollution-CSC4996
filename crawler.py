import requests
from bs4 import BeautifulSoup as soup
import database
import newspaper


class Crawler:
    def __init__(self):
        self.baseUrl = ""
        self.keywords = []
        self.articleLinks = []
        self.homePageArticleLinks = []
        self.articleCount = 0

    def crawl(self):
        print("Crawling: " + self.baseUrl)
        links = []
        for keyword in self.keywords:
            query = self.searchQuery.replace("PEATKEY", keyword).replace("PEATPAGE","1")

            page = requests.get(query)

            soupLinks = self.scrapeArticleLinks(page)

            for link in soupLinks:
                if link['href'] not in links:
                    links.append(link['href'])
                    self.articleCount = self.articleCount + 1

        self.articleLinks = self.filterLinksForArticles(links)
        self.storeInUrlsCollection(self.articleLinks)

    def crawlHomePage(self):
        links = newspaper.build('https://thecountypress.mihomepaper.com/', memoize_articles=False)
        for article in links.articles:
            self.homePageArticleLinks.append(article.url)
        self.storeInUrlsCollection(self.homePageArticleLinks)

    def filterLinksForArticles(self, links):
        return links

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