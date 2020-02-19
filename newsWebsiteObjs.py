from newsWebsite import NewsWebsite

newsWebsiteObjList = []

# newsWebsiteObjList.append(NewsWebsite("https://www.stignacenews.com",
#                                       "title", "", "", "https://www.stignacenews.com/page/PEATPAGE/?s=PEATKEY",
#                                       "/articles/", False))

newsWebsiteObjList.append(NewsWebsite("https://www.ourmidland.com", "title", "p", "time",
                                      "https://www.ourmidland.com/search/?action=search&searchindex=solr&query=PEATKEY&page=PEATPAGE",
                                      "/news/article/", False))

newsWebsiteObjList.append(NewsWebsite("https://www.michigansthumb.com/", "title", "p", "time",
                                      "https://www.michigansthumb.com/search/?action=search&searchindex=solr&query=PEATKEY&page=PEATPAGE",
                                      "/news/article", False))

def getNewsWebsiteObjsList():
    return newsWebsiteObjList


#################### For Testing ###########################

def getNewsWebsiteObjsListForTesting():
    newsWebsiteObjList = []
    newsWebsiteObjList.append(NewsWebsite("https://www.ourmidland.com", "title", "p", "time",
                                          "https://www.ourmidland.com/search/?action=search&searchindex=solr&query=PEATKEY&page=PEATPAGE",
                                          "/news/article/", False))
    return newsWebsiteObjList