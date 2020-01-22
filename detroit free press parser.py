# Detroit Free Press Parser 

import requests 
from bs4 import BeautifulSoup as soup

class FreepCrawler():
	def __init__(self, *keywords):
		self.urls = []
		self.baseURLs = []
		self.keywords = []

		for key in keywords:
			self.keywords.append(key)
			self.baseURLs.append("https://www.freep.com/search/" + key + ".com")

	def printURLs(self):
		for url in self.baseURLs:
			print(url)

	def getURLs(self):
		for url in self.baseURLs:
			page = requests.get(url)
			soup_page = soup(page.content, 'html.parser')
			hrefs = soup_page.find_all('a', href=True)
			
			for href in hrefs:
				print(href['href'])
				print("\n")

		return self.urls


class FreepScraper:
	def __init__(self, url):
		self.articleURL = url 
		self.articleTitle = ""
		self.articleBody = []

	def setArticleTitle(self, articleTitle):
		self.articleTitle = articleTitle

	def setURL(self, url):
		self.articleURL = url

	def setArticleBody(sel):
		self.articleBody = body

	def getArticleTitle(self):
		return self.articleTitle

	def getArticleURL(self):
		return self.articleURL

	def getArticleBody(self):
		return self.articleBody

	def printArticleBody(self):
		for body in self.articleBody:
			print(body + "\n")

	def scrape(self):
		page = requests.get(self.articleURL)
		soup_page = soup(page.content, 'html.parser')

		self.articleTitle = soup_page.find_all(class_="util-bar-share-summary-title")[0].get_text()

		body = soup_page.find_all(class_="p-text")

		for paragraph in body:
			self.articleBody.append(paragraph.get_text())


scraper_test = FreepScraper("https://www.freep.com/story/news/local/michigan/" + 
	"detroit/2019/12/05/detroit-bulk-storage-revere-copper-detroit-river-uranium/2618868001/")

spider_test = FreepCrawler("pollution")
print(spider_test.getURLs())





