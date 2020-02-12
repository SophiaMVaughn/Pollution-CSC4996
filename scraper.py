
################################################
#                Scraper Class                 #
################################################

class Scraper:
    def __init__(self, url, websiteObjList):
        self.articleURL = url
        self.websiteObjList = websiteObjList

        websiteName = url.split("www.")[1].split(".com")[0]

        for website in websiteObjList:
            if websiteName == website.getWebsiteName():
                self.website = website
                self.scrape()

    def scrape(self):
        print("[+] Scraping " + self.articleURL)


