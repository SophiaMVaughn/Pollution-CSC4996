
def getUrls(baseUrl):
    links = []
    if baseUrl == "https://www.ourmidland.com/":
        links.append("https://www.ourmidland.com/news/article/UPDATE-Pine-River-spill-determined-to-be-15086305.php")
        links.append("https://www.ourmidland.com/news/article/City-Oil-slick-on-Pine-River-15084185.php")
        links.append("https://www.ourmidland.com/news/article/Clean-up-efforts-continue-on-Bush-Creek-15089825.php")
        links.append("https://www.ourmidland.com/news/article/Virginia-issues-violation-notice-to-Dominion-for-6906076.php")
        links.append("https://www.ourmidland.com/news/article/Tanker-rolls-on-Homer-Adams-15098387.php")

    elif baseUrl == "http://www.marion-press.com/":
        pass

    elif baseUrl == "https://thecountypress.mihomepaper.com/":
        links.append("https://thecountypress.mihomepaper.com/articles/deputy-director-at-msp-announces-jan-27-retirement/")

    elif baseUrl == "https://www.lakecountystar.com/":
        links.append(
            "https://www.lakecountystar.com/news/article/Official-Pine-River-spill-nbsp-is-dielectric-15086338.php")
        links.append("https://www.lakecountystar.com/news/article/UPDATE-Pine-River-spill-determined-to-be-15086305.php")
        links.append(
            "https://www.lakecountystar.com/business/energy/article/Decades-after-oil-spill-Barnett-Shale-lake-15073316.php")
        links.append(
            "https://www.lakecountystar.com/news/article/45-000-gallons-of-raw-sewage-spills-near-creek-15070289.php")
        links.append(
            "https://www.lakecountystar.com/news/article/Semi-crashes-in-Montana-river-spilling-diesel-15067701.php")
        links.append(
            "https://www.lakecountystar.com/news/article/Highway-22-closed-after-tanker-crash-diesel-spill-15063079.php")
        links.append(
            "https://www.lakecountystar.com/news/medical/article/211M-gallons-of-sewage-spilled-into-Florida-city-15061667.php")

    elif baseUrl == "https://www.northernexpress.com/":
        pass

    elif baseUrl == "https://www.manisteenews.com/":
        links.append(
            "https://www.manisteenews.com/editorials/article/Time-to-protect-Great-Lakes-from-oil-spill-is-now-14221909.php")
        links.append(
            "https://www.manisteenews.com/state-news/article/Report-slams-Enbridge-Energy-s-history-of-oil-14228360.php")
        links.append("https://www.manisteenews.com/news/article/Official-Pine-River-spill-nbsp-is-dielectric-15086338.php")
        links.append("https://www.manisteenews.com/news/article/UPDATE-Pine-River-spill-determined-to-be-15086305.php")

    elif baseUrl == "https://michiganchronicle.com/":
        pass

    elif baseUrl == "https://clarkstonnews.com/":
        pass

    elif baseUrl == "https://www.harborlightnews.com/":
        pass

    elif baseUrl == "https://thedailynews.cc/":
        pass

    elif baseUrl == "https://lakeorionreview.com/":
        pass

    elif baseUrl == "https://www.leelanaunews.com/":
        links.append("https://www.leelanaunews.com/articles/chemical-scare-in-elmwood-leads-to-evacuations/")

    elif baseUrl == "https://www.houghtonlakeresorter.com/":
        pass
    elif baseUrl == "https://www.ironmountaindailynews.com/":
        links.append("https://www.ironmountaindailynews.com/news/local-news/2019/07/sewage-spills-into-escanaba-river/")

    elif baseUrl == "https://www.miningjournal.net/":
        links.append(
            "https://www.miningjournal.net/news/michigan-news-apwire/2019/12/some-metals-not-found-in-river-spill/")
        links.append("https://www.miningjournal.net/news/michigan-news-apwire/2019/12/radiation-levels-ok-at-river-spill/")
        links.append(
            "https://www.miningjournal.net/news/front-page-news/2018/07/report-lake-oil-spill-in-michigan-would-cost-nearly-2b/")
        links.append(
            "https://www.miningjournal.net/news/2018/03/repairs-cleanup-completed-after-krist-oil-co-gas-station-fuel-spill/")

    elif baseUrl == "https://www.thealpenanews.com/":
        links.append(
            "https://www.thealpenanews.com/news/michigan-news-apwire/2020/01/epa-lead-uranium-found-after-detroit-river-spill/")
        links.append("https://www.thealpenanews.com/news/local-news/2019/07/gas-spill-in-the-thunder-bay-river/")
        links.append(
            "https://www.thealpenanews.com/news/national-news-apwire/2017/09/evidence-of-spills-at-toxic-site-during-floods/")

    return links