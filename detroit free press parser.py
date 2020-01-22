# Detroit Free Press Parser 

import requests 
from bs4 import BeautifulSoup as soup

class FreepScraper:
	def __init__(self, url):
		self.articleURL = url 

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
		self.page = requests.get(self.articleURL)
		soup_page = soup(self.page.content, 'html.parser')

	def getScraped(self):
		return soup(self.page.content, 'html.parser')


test = FreepScraper("https://www.freep.com/story/news/local/michigan/" + 
	"detroit/2019/12/05/detroit-bulk-storage-revere-copper-detroit-river-uranium/2618868001/")

test.scrape()
print(test.getScraped())

# page = requests.get("https://www.freep.com/story/news/local/michigan/" + 
# 	"detroit/2019/12/05/detroit-bulk-storage-revere-copper-detroit-river-uranium/2618868001/")

# soup_page = soup(page.content, 'html.parser')

# print(soup_page.prettify()) 



