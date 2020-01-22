# Detroit Free Press Parser 

import requests 
from bs4 import BeautifulSoup as soup

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

	def scrape(self):
		page = requests.get(self.articleURL)
		soup_page = soup(page.content, 'html.parser')

		self.articleTitle = soup_page.find_all(class_="util-bar-share-summary-title")[0].get_text()

		self.articleBody = soup_page.find_all(class_="p-text")

		for body in self.articleBody:
			print(body.get_text())
			print("\n")

	def getScraped(self):
		return soup(self.page.content, 'html.parser')


test = FreepScraper("https://www.freep.com/story/news/local/michigan/" + 
	"detroit/2019/12/05/detroit-bulk-storage-revere-copper-detroit-river-uranium/2618868001/")

test.scrape()
# print(test.getScraped())

# page = requests.get("https://www.freep.com/story/news/local/michigan/" + 
# 	"detroit/2019/12/05/detroit-bulk-storage-revere-copper-detroit-river-uranium/2618868001/")

# soup_page = soup(page.content, 'html.parser')

# print(soup_page.prettify()) 





