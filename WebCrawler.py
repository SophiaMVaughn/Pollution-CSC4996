import requests
from bs4 import BeautifulSoup as soup, BeautifulSoup, SoupStrainer
import time
from selenium import webdriver
# Gets the all urls from a website
from selenium.webdriver.chrome.options import Options

# Launches a chrometab which goes to all the urls that were specified.
def goToSearchUrl(link):
    chrome_options1 = Options()
    chrome_options1.add_argument("--headless")
    chrome_options1.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36')
    driver = webdriver.Chrome('C:/Users/mhere/OneDrive/Desktop/chromedriver', options=chrome_options1)
    page1=driver.get(link)
    pageSource=driver.page_source
    time.sleep(3)
    driver.quit()
    return pageSource

# Allows us to change the keyword for every website we need to collect data on.
def readFromFile(key):
    urls = []
    with open("WebLinks.txt", "r") as file:
        for line in file:
            #Imports the words from the key file to replace the keyword in every search url
            with open("Keyword.txt", "r") as keyFile:
                for key in keyFile:
                    line.replace("Pollution", key)
                    urls.append(line.replace("Pollution", key).rstrip())
    return urls


def readFromFileClasses():
    classes = []
    with open("Classes.txt", "r") as file:
        for line in file:
            classes.append(line.rstrip())
    return classes

# Allows the user to input a keyword to see what articles are on each site.
key= []
print(key)
finalUrls = readFromFile(key)
finalClasses = readFromFileClasses()
dict = {}
for x in range(len(finalClasses)):
    className=finalClasses[x]
    url=finalUrls[x]
    dict1 = {url:className}
    dict.update(dict1)
print(dict)
results=[]
f = open("Results.txt", "w")
for url in dict:
    page=goToSearchUrl(url)
    classSearchTerm =dict.get(url)
    soup = BeautifulSoup(page, 'html.parser')
    weblinks=soup.find_all(True, {'class': [finalClasses]})
    for weblink in weblinks:
        results.append(str(weblink.find("a", href=True)).split('"', 2)[1])
        f.writelines(str(weblink.find("a", href=True)).split('"', 2)[1])
        f.writelines('\n')
        print(str(weblink.find("a", href=True)).split('"', 2)[1])
f.close()

