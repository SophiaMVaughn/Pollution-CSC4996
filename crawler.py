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

        print("\n[+] Crawling...\n")

        for keyword in self.keywords:
            print("[+] Crawling " + self.website.getWebsiteName() + ".com for keyword \'%s\'...\n" % keyword)
            searchURL = self.website.getSearchQuery(keyword, 1)
            page = requests.get(searchURL)
            soupPage = soup(page.content, 'html.parser')

            links = soupPage.find_all('a', href=True)

            for link in links:
                if self.website.getArticleLinkStructure() in link['href']:
                    self.urlsCrawled.append(link['href'])

    def getCrawledURLs(self):
        return self.urlsCrawled

