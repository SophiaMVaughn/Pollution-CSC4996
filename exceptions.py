class WebsiteFailedToInitialize(Exception):
    def __init__(self, url):
        self.url = url
    def __str__(self):
        return "Failed to initialize website: " + self.url

class NextPageException(Exception):
    def __init__(self, url):
        self.url = url
    def __str__(self):
        return "Failed to request next page: " + self.url