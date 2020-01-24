# Detroit Free Press Parser 

import requests 
from bs4 import BeautifulSoup as soup

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
						self.urls.append("https://www.freep/" + link['href'])

		except requests.exceptions.ConnectionError:
			print("[-] Connection refused: too man requests")

	# for each url in the urls list, scrape its content and store in scrapedArticles list as FreepScraper objects
	def scrapeURLs(self):
		for url in self.urls:
			article = FreepScraper(url)
			self.scrapedArticles.append(article.scrape())

	def getURLs(self):
		return self.urls

	def getScrapedArticle(self, index):
		if index >= 0 and index < len(self.scrapedArticles):
			return self.scrapedArticles[index]
		else:
			print("[-] Index out of range. Acceptable range: 0-" + str(len(self.scrapedArticles)-1))

class FreepScraper:

	# initialize variables
	def __init__(self, url):
		self.articleURL = url 
		self.articleTitle = ""
		self.articleBody = []

	# set the article title to articleTitle param
	def setArticleTitle(self, articleTitle):
		self.articleTitle = articleTitle

	# set the article url to url param
	def setURL(self, url):
		self.articleURL = url

	# set the article body to body param
	def setArticleBody(self, body):
		self.articleBody = body

	# return the article title
	def getArticleTitle(self):
		return self.articleTitle

	# return the article url
	def getArticleURL(self):
		return self.articleURL

	# return the article body
	def getArticleBody(self):
		return self.articleBody

	# print the article body
	def printArticleBody(self):
		for body in self.articleBody:
			print(body + "\n")

	# scrape and store article title and body. Save article body as array of paragraphs
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
spider_test.crawlURLs()
# print(spider_test.getScrapedArticle(0).getArticleTitle() + "\n\n")
# print(spider_test.getScrapedArticle(0).getArticleBody())






