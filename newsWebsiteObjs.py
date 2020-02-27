from newsWebsite import NewsWebsite

# https://www.candgnews.com/
# https://www.mlive.com/
# https://www.leaderpub.com/
# http://www.marion-press.com/
# https://thecountypress.mihomepaper.com/
# https://www.lakecountystar.com/
# https://www.record-eagle.com/
# https://www.macombdaily.com/
# https://www.northernexpress.com/
# https://www.manisteenews.com/
# https://www.theoaklandpress.com/
# https://www.shorelinemedia.net/
# https://michiganchronicle.com/
# https://clarkstonnews.com/
# https://www.harborlightnews.com/
# https://thedailynews.cc/
# https://lakeorionreview.com/
# https://www.leelanaunews.com/
# https://www.houghtonlakeresorter.com/
# https://www.detroitnews.com/
# https://www.freep.com/
# https://www.thetimesherald.com/
# https://www.ironmountaindailynews.com/
# https://www.miningjournal.net/
# https://www.thealpenanews.com/


#################### For actual running ###########################

newsWebsiteObjList = []

newsWebsiteObjList.append(NewsWebsite("https://www.stignacenews.com", "title", "", "", "https://www.stignacenews.com/page/PEATPAGE/?s=PEATKEY", "/articles/", False))
newsWebsiteObjList.append(NewsWebsite("https://www.ourmidland.com", "title", "p", "time", "https://www.ourmidland.com/search/?action=search&searchindex=solr&query=PEATKEY&page=PEATPAGE", "/news/article/", False))
newsWebsiteObjList.append(NewsWebsite("https://www.michigansthumb.com/", "title", "p", "time", "https://www.michigansthumb.com/search/?action=search&searchindex=solr&query=PEATKEY&page=PEATPAGE", "/news/article", False))
# TODO: fix this object
newsWebsiteObjList.append(NewsWebsite("https://www.grbj.com/", "title", "p", "date", "https://www.grbj.com/search?exclude_datatypes%5B%5D=video&exclude_datatypes%5B%5D=file&page=PEATPAGE&q=PEATKEY", "/articles/", False))


def getNewsWebsiteObjsList():
    return newsWebsiteObjList


#################### For Testing ###########################

def getNewsWebsiteObjsListForTesting():
    websiteList = []
    websiteList.append(newsWebsiteObjList[3])
    return websiteList

