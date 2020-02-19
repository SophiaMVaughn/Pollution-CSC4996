import requests
from bs4 import BeautifulSoup as soup

################################################
#                Crawler Class                 #
################################################

class Crawler:
    def __init__(self, websiteObj, *keywords):

        self.website = websiteObj

        # all the article urls crawled by the crawler
        self.urlsCrawled = []

        # all search keywords
        self.keywords = []

        for key in keywords:
            self.keywords.append(key)

        self.crawl()


    def crawl(self):

        for keyword in self.keywords:
            print("[+] Crawling " + self.website.getWebsiteName() + ".com for keyword \'%s\'" % keyword)
            searchURL = self.website.getSearchQuery(keyword, 1)
            page = requests.get(searchURL)
            soupPage = soup(page.content, 'html.parser')

            links = soupPage.find_all('a', href=True)

            for link in links:

                link = link['href']

                if self.website.getURL() not in link:
                    link = self.website.getURL() + link

                if (self.website.getURL() + self.website.getArticleLinkStructure()) in link:
                    self.urlsCrawled.append(link)

    def getCrawledURLs(self):
        return self.urlsCrawled

