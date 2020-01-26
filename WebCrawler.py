import requests
from bs4 import BeautifulSoup as soup, BeautifulSoup, SoupStrainer
import time
from selenium import webdriver

# Gets the all urls from a website
def getUrls():
    URL = 'https://www.usnpl.com/search/state?state=MI#section-D'
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, 'html.parser')
    links = SoupStrainer('a')

    # Find the class which holds the correct web links
    websites = soup.find_all(True, {'class': ['w-10']})
    unFilteredWebsites = []
    # Filter out all unnecessary tags
    for tag in websites:
        tdTags = tag.find_all("a")
        if tdTags:
            unFilteredWebsites.append(tdTags)
    filteredWebsites = []
    for it in unFilteredWebsites:
        formattedWebsite = str(it).split('"', 2)[1]
        # remove facebook, twitter and instagram hrefs
        if not (formattedWebsite.__contains__("twitter") or formattedWebsite.__contains__(
                "facebook") or formattedWebsite.__contains__("instagram") or formattedWebsite.__contains__("youtube")):
            filteredWebsites.append(formattedWebsite)
    return filteredWebsites


# Launches a chrometab which goes to all the urls that were specified.
def goToSearchUrl(link):
    driver = webdriver.Chrome('C:/Users/mhere/OneDrive/Desktop/chromedriver')
    driver.get(link)
    time.sleep(5)
    driver.quit()


# Allows us to change the keyword for every website we need to collect data on.
def readFromFile(keyword):
    urls = []
    with open("WebLinks.txt", "r") as file:
        for line in file:
            line.replace("Pollution", keyword)
            urls.append(line.replace("Pollution", keyword).rstrip())
    return urls


# Allows the user to input a keyword to see what articles are on each site.
keyword = input("Enter a keyword to search for : ")
print(keyword)
finalUrls = readFromFile(keyword)
print(finalUrls)
for url in finalUrls:
    goToSearchUrl(url)
