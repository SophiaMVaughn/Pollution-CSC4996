##from officialComm import officialComment
##import unittest
##
##
##class testOfficialComment(unittest.TestCase):
##    def testOffComm(self):
##        oc = officialComment(['LAS VEGAS (AP) —', 'State officials who monitor chemical contaminations at 40 sites in southern Nevada are now preparing for a large-scale cleanup at one that stemmed from a spill at a dry-cleaning shop decades ago.', 'The Las Vegas Sun reports (http://bit.ly/29F2AWA ) that more than 200 homes sit atop a plume created years ago at a dry-cleaning operation.', 'The cancer-causing chemical bled into groundwater after a 1982 spill, and officials say the plume now stretches more than a mile long.', 'State regulators hope to begin extracting the perchloroethylene, or PCE, by spring of 2017.', 'Recently they have installed mitigating systems to keep the chemical out of homes.', 'Regulators are in the process of finalizing that plan with the former owners of the Maryland Square property, who were found responsible to pay for the cleanup.', '___ Information from: Las Vegas Sun, http://www.lasvegassun.com'])
##        
##        self.assertListEqual(
##            ['The cancer-causing chemical bled into groundwater after a 1982 spill, and officials say the plume now stretches more than a mile long.'],
##            oc[0])
##
##
##unittest.main()
##
##
##
##from RNNBinary import readBinary
##
##class testBinaryReading(unittest.TestCase):
##    def testRNNBinary(self):
##        chem, quant = readBinary(['GILLETTE, Wyo.', '(AP) — Officials say a pipeline leak that caused between 1,200 and 1,700 gallons of crude oil to spill into a creek near Gillette has been clamped to prevent further leakage.', 'The Gillette News Record reports (http://bit.ly/20FxCzB ) that the Wyoming Department of Environmental Quality has blamed the leak that was reported Sunday on internal corrosion of the pipeline.', 'A spokesman for Belle Fourche Pipeline, Bill Salvin, says the company is still investigating the leak to determine an official cause.', 'The oil had covered about a quarter mile of Timber Creek in northern Campbell County and leaked under a railroad and through a culvert.', 'Belle Fourche employees worked to burn most of the oil out of the water Monday.', 'Salvin says the cleanup will last a couple more days.', '___ Information from:', 'The Gillette (Wyo.)', 'News Record, http://www.gillettenewsrecord.com'])
##            
##        self.assertListEqual(
##            ['CRUDE OIL', 'OIL'],
##            chem)
##        
##        
##unittest.main()


##from scraper import Scraper
##import unittest
##
##class testScraper(unittest.TestCase):
##    def testScrapeObj(self):
##        scrapeObj = Scraper('https://www.mlive.com/news/grand-rapids/2019/08/coal-ash-from-west-michigan-power-plant-might-be-contaminating-drinking-water-wells.html')
##        articleObj = scrapeObj.getScrapedArticle()
##        self.assertEqual(str(articleObj['url']),'https://www.mlive.com/news/grand-rapids/2019/08/coal-ash-from-west-michigan-power-plant-might-be-contaminating-drinking-water-wells.html')
##        self.assertEqual(str(articleObj['title']), 'Coal ash from West Michigan power plant might be contaminating drinking water wells - mlive.com')
##        self.assertEqual(str(articleObj['publishingDate']), "")
##        self.assertEqual(str(articleObj['body']), ' Sierra Club releases results of contaminated drinking water test WEST OLIVE, MI -- Some residents and environmental advocates are raising alarms about potential drinking water contamination they say may be caused by a nearby coal-fired power plant in West Michigan. Sierra Club officials announced Tuesday that one of four private drinking wells tested near Consumers Energy’s J.H. Campbell coal power plant in West Olive was positive for arsenic at levels more than two times higher than federal drinking water standards. “Long-term exposure to high levels of arsenic in drinking water can cause several types of cancer and skin disorders and can also increase risks for diabetes and high blood pressure,” according to the U.S. Environmental Protection Agency. Metals like barium, radium, yttrium and lead were also found in the wells but at “moderate levels" not violating drinking water standards, Sierra Club officials said. Sierra Club officials hazarded that the tests are only a small sampling and not comprehensive enough to pinpoint a source -- although they believe it could be the now-defunct unlined coal ash pits at the power plant. Consumers Energy disputes the environmental groups’ theory about the source of the contamination. Coal ash is the by-product of burning coal. If not properly managed, it can pollute groundwater with contaminants such as mercury, cadmium and arsenic, according to the EPA. Before 2015, utilities were legally allowed to store coal ash in unlined pits, Charlotte Jameson, energy policy and legislative affairs director for the Michigan Environmental Council, said. Jan O’Connell, development director and energy issues organizer at Sierra Club, said her group has forwarded the test results to the Michigan Department of Environment, Great Lakes and Energy, hoping that state regulators will conduct further and more comprehensive testing. EGLE spokesperson Scott Dean said he couldn’t comment on the data because EGLE officials haven’t seen the test reports. Dean said the location of the wells is important to know, as arsenic is naturally occurring in many areas of the state and associated as well with past farming activity. “We have an extensive monitoring network and results from sampling for the current and historic disposal areas, plus we have a remedial action plan for the historic disposal area,” Dean said of the coal plant site. Consumers Energy, in a statement, said the company monitors groundwater at the plant and has no indication of contamination from formerly used coal ash pits migrating off the property. “Our data indicates no exceedances of arsenic, lead or radium above drinking-water standards migrating beyond Consumers Energy’s property boundary," according to Consumers Energy’s statement. "We will continue to review this information and work proactively with the Michigan Department of Environment, Great Lakes and Energy and our community.” Jameson argues that Consumers Energy’s own monitoring well data from 2017 shows some on-property migration from the pits of groundwater contaminated with arsenic exceeding EPA guidelines. The testing showed arsenic levels in groundwater four times higher than the EPA’s safe drinking-water standards, she said. “It’s clear that the Campbell coal plant is responsible for contaminating groundwater and surface water in the vicinity of the plant,” she said. “EGLE should fully investigate the area’s drinking water wells to ensure that toxic groundwater contamination throughout Campbell is not polluting drinking water in the area." The home with arsenic exceeding federal drinking water standards is located south of the power plant on the south shore of Pigeon Lake. All four homes tested in the area of Pigeon Lake had “moderate” to “low” levels of radium. Two of the homes are north of Pigeon Lake, and the last one is located on its eastern shores. Sierra Club officials declined to give the exact locations, citing privacy concerns. The Grand Rapids municipal water system’s Lake Michigan filtration plant is located about 4 miles north of the power plant. The plant, which serves about 300,000 people, draws its water about a mile out from shore. Arsenic, lead and radium are not present in the water supply at detectable levels, said Mike Grenier, superintendent of the Lake Michigan filtration plant. Lead is present but in areas of lead service lines and below action levels, he said. Barium is present in the system in minute amounts just above the detection limit and far below drinking water standards. Jameson and O’Connell called on Consumers to shut down the coal power plant sooner than 2040, which is the company’s current timeline, as well as remove all coal ash from the unlined pits. Roger Morgenstern, a Consumers Energy spokesperson, said the company has removed coal ash from every storage pond at the power plant. All coal ash currently being generated is either being reused or placed in a double-lined landfill at the power plant site. Note to readers: if you purchase something through one of our affiliate links we may earn a commission. Registration on or use of this site constitutes acceptance of our User Agreement, Privacy Policy and Cookie Statement, and Your California Privacy Rights (each updated 1/1/20). © 2020 Advance Local Media LLC. All rights reserved (About Us). The material on this site may not be reproduced, distributed, transmitted, cached or otherwise used, except with the prior written permission of Advance Local. Community Rules apply to all content you upload or otherwise submit to this site. Ad Choices')
##unittest.main()
##
##
##from scraper import Scraper
##import unittest
##
##class testScraper(unittest.TestCase):
##    def testScrapeObj(self):
##        scrapeObj = Scraper('https://www.mlive.com/news/grand-rapids/2019/08/coal-ash-from-west-michigan-power-plant-might-be-contaminating-drinking-water-wells.html')
##        self.assertEqual(str(articleObj['publishingDate']), "")
##        
##unittest.main()
##
##import database
##import unittest
##from pymongo import MongoClient
##class testDatabase(unittest.TestCase):
##    def testIncidents(self):
##        database.Incidents(
##                chemicals=["Carbon Dioxide"],
##                date="12/22/2019",
##                location="Wayne State University",
##                officialStatement=["This is the official statement"],
##                articleLinks=["www.test1.com"]
##            ).save()
##        
##        client = MongoClient("mongodb://127.0.0.1:27017")
##        db = client.Pollution
##        collection = db.incidents
##        test_event = collection.find({'articleLinks': ['www.test1.com']})
##        for t in test_event:
##            print(t)
##            
##
##
##unittest.main()
##
##
##import database
##import unittest
##from pymongo import MongoClient
##class testDatabaseClass(unittest.TestCase):
##    def testArticleCollection(self):
##        database.Articles(
##                url="www.testurl.com",
##                title="test article title",
##                publishingDate="12/12/12"
##            ).save()
##        
##        client = MongoClient("mongodb://127.0.0.1:27017")
##        db = client.Pollution
##        collection = db.articles
##        test_event = collection.find({'url': 'www.testurl.com'})
##        for t in test_event:
##            print(t)
##            
##
##
##unittest.main()
##
##
##import database
##import unittest
##from pymongo import MongoClient
##class testDatabaseClass(unittest.TestCase):
##    def testErrorCollection(self):
##        database.Errors(
##                url="www.testurl.com",
##                errorID="5e6e1de56fd9c4c9467f03b1",
##                publishingDate="12/12/12"
##            ).save()
##        
##        client = MongoClient("mongodb://127.0.0.1:27017")
##        db = client.Pollution
##        collection = db.errors
##        test_event = collection.find({'url': 'www.testurl.com'})
##        for t in test_event:
##            print(t)
##            
##
##unittest.main()


import database
import unittest
from scraperInterface import ScraperInterface
from pymongo import MongoClient
class testErrors(unittest.TestCase):
    def testErrorCollect(self):
        keywords = [""]
        scraper = ScraperInterface(keywords)
        scraper.storeInIncidentsCollection(["Carbon Dioxide"], "12/22/2019", "", ["This is the official statement"], ["www.locationerror.com"])
        
        client = MongoClient("mongodb://127.0.0.1:27017")
        db = client.Pollution

        #should come back with the test entry with the error message of "no location"
        collection = db.errors
        test_event = collection.find({'articleLinks': ['www.locationerror.com']})
        for t in test_event:
            print(t)

        #should come back blank
        collection = db.incidents
        test_event = collection.find({'articleLinks': ['www.locationerror.com']})
        for t in test_event:
            print(t)


unittest.main()



import database
import unittest
from scraperInterface import ScraperInterface
from pymongo import MongoClient
class testErrors(unittest.TestCase):
    def testErrorCollect(self):
        keywords = [""]
        scraper = ScraperInterface(keywords)
        scraper.storeInIncidentsCollection([], "12/22/2019", "Detroit", ["This is the official statement"], ["www.chemicalerror.com"])
        
        client = MongoClient("mongodb://127.0.0.1:27017")
        db = client.Pollution
        
        #should come back with the test entry with the error message of "no chemical"
        collection = db.errors
        test_event = collection.find({'articleLinks': ['www.chemicalerror.com']})
        for t in test_event:
            print(t)

        #should come back blank
        collection = db.incidents
        test_event = collection.find({'articleLinks': ['www.chemicalerror.com']})
        for t in test_event:
            print(t)


unittest.main()

