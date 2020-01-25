# Detroit Free Press Crawler

import requests 
from bs4 import BeautifulSoup as soup
from freepScraper import FreepScraper

class FreepCrawler():

	# initialize variables and create list of base urls with the different search keywords
	def __init__(self, *keywords):
		self.urls = []
		self.baseURLs = []
		self.keywords = []
		self.scrapedArticles = []

		for key in keywords:
			self.keywords.append(key)
			self.baseURLs.append("https://www.freep.com/search/" + key + "/")

	# print all urls that have been crawled
	def printURLs(self):
		for url in self.urls:
			print(url)

	# for each base url, crawl all article links contained in each.  For instance, base url is the search result for polution,
	# so crawlURLs() will retrieve article urls from that page and append them to the urls list
	def crawlURLs(self):
		try:
			for url in self.baseURLs:
				page = requests.get(url)
				soup_page = soup(page.content, 'html.parser')
				links = soup_page.find_all('a', href=True)

				for link in links:
					if "/story/news/local/michigan/" in link['href']:
						self.urls.append("https://www.freep.com" + link['href'])

		except requests.exceptions.ConnectionError:
			print("[-] Connection refused: too man requests")

	# for each url in the urls list, scrape its content and store in scrapedArticles list as FreepScraper objects
	def scrapeURLs(self):
		for url in self.urls:
			print("scraping " + str(url))
			article = FreepScraper(url)
			self.scrapedArticles.append(article)
		print("\n\n")

	def getURLs(self):
		return self.urls

	def getScrapedArticles(self):
		return self.scrapedArticles

	def getScrapedArticle(self, index):
		if index >= 0 and index < len(self.scrapedArticles):
			return self.scrapedArticles[index]
		else:
			print("[-] Index out of range. Acceptable range: 0-" + str(len(self.scrapedArticles)-1))








