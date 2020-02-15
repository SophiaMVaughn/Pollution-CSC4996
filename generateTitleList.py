from bs4 import BeautifulSoup as soup
import requests
from time import sleep

urls_list = open('myUrlList.txt','r').readlines()

urls = []

for url in urls_list:
	urls.append(url.strip())

titles = open('article-titles.txt', 'a+')

count = 1
for url in urls:
	if count > 3045:
		page = requests.get(url)
		soup_page = soup(page.content, 'html.parser')
		title = soup_page.find_all("title")[0].get_text()
		titles.write(title + '\n')
		print(title)
	count = count + 1
