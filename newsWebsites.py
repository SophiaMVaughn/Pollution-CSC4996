
################################################
#               NewsWebsite Class              #
################################################

class NewsWebsite:
    def __init__(self, articleURL, titleTag, bodyTag, publishingDateTag, nextPageTag, articleLinkStructure, infiniteScrolling):
        self.articleURL = articleURL
        self.titleTag = titleTag
        self.bodyTag = bodyTag
        self.publishingDateTag = publishingDateTag
        self.nextPageTag = nextPageTag
        self.articleLinkStructure = articleLinkStructure
        self.infiniteScrolling = infiniteScrolling

    def getURL(self):
        return self.articleURL

    def getTitleTag(self):
        return self.titleTag

    def getBodyTag(self):
        return self.bodyTag

    def getPublishingDateTag(self):
        return self.publishingDateTag

    def getNextPageTag(self):
        return self.nextPageTag

    def getArticleLinkStructure(self):
        return self.articleLinkStructure

    def getInfiniteScrolling(self):
        return self.infiniteScrolling

    def getSearchQuery(self, keyword, pageNum):
        if "stignacenews" in self.articleURL:
            return "https://www.stignacenews.com/page/" + str(pageNum) + "/?s=" + keyword

    def getWebsiteName(self):
        websiteName = self.articleURL.split("www.")[1].split(".com")[0]
        return websiteName


