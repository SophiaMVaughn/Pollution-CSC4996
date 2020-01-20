# Detroit Free Press Parser 

import requests 
from bs4 import BeautifulSoup as soup

page = requests.get("https://www.freep.com/story/news/local/michigan/" + 
	"detroit/2019/12/05/detroit-bulk-storage-revere-copper-detroit-river-uranium/2618868001/")

soup_page = soup(page.content, 'html.parser')

print(soup_page.prettify())