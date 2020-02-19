
################################################
#               NewsWebsite Class              #
################################################

class NewsWebsite:
    def __init__(self, articleURL, titleTag, bodyTag, publishingDateTag, searchSyntax,
                 articleLinkStructure, infiniteScrolling):
        self.articleURL = articleURL
        self.titleTag = titleTag
        self.bodyTag = bodyTag
        self.publishingDateTag = publishingDateTag
        self.searchSyntax = searchSyntax
        self.articleLinkStructure = articleLinkStructure
        self.infiniteScrolling = infiniteScrolling

    # return the base URL of the website
    def getURL(self):
        return self.articleURL

    # returns the tag used to identify an article title
    def getTitleTag(self):
        return self.titleTag

    # returns the tag used to identify the body of an article
    def getBodyTag(self):
        return self.bodyTag

    # returns the tag used to identify the article publishing date
    def getPublishingDateTag(self):
        return self.publishingDateTag

    # returns the URLs structure of article links.  For instance, stignacenews articles
    # have "www.stignacenews.com/articles/..." in their article URLs, therefore for this website it
    # would return /articles/
    def getArticleLinkStructure(self):
        return self.articleLinkStructure

    # returns True is website implements infinite scrolling and returns False if it doesn't
    def infiniteScrollingEnabled(self):
        return self.infiniteScrolling

    # returns the search query structure that the website uses. Takes the keyword to search for and
    # the page number to search within (if infinite scrolling used, then pageNum will be 0 as default)
    def getSearchQuery(self, keyword, pageNum=0):
        search = self.searchSyntax.replace("PEATKEY", keyword).replace("PEATPAGE", str(pageNum))
        return search

    def getWebsiteName(self):
        websiteName = self.articleURL.split("www.")[1].split(".com")[0]
        return websiteName


