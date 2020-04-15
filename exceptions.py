# failure to connect to website
class WebsiteFailedToInitialize(Exception):
    def __init__(self, url):
        self.url = url

    def __str__(self):
        return "Failed to initialize website: " + self.url

# failure to query next page of search page
class NextPageException(Exception):
    def __init__(self, url):
        self.url = url

    def __str__(self):
        return "Failed to request next page: " + self.url
