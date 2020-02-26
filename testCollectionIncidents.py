import database

def populateDatabase():
    database.Incidents(
        chemicals=["Oil", "Benzene"],
        date="11/08/2020",
        location="Detroit river",
        officialStatement="This is the official statement",
        articleLinks=["www.test.com"]
    ).save()

    database.Incidents(
        chemicals=["Carbon Dioxide"],
        date="12/22/2019",
        location="Wayne State University",
        officialStatement="This is the official statement",
        articleLinks=["www.test1.com", "www.test2.com"]
    ).save()

    database.Incidents(
        chemicals=["cadmium", "mercury", "lead"],
        date="03/14/2020",
        location="Clinton Township",
        officialStatement="This is the official statement",
        articleLinks=["www.test1.com", "www.test2.com"]
    ).save()

