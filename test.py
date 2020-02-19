import requests
from bs4 import BeautifulSoup as soup

page = requests.get("https://www.stignacenews.com/articles/graymont-will-build-plant/")
soup_page = soup(page.content, 'html.parser')

articleTitle = soup_page.find_all("title")[0].get_text()

body = soup_page.find_all("p")
