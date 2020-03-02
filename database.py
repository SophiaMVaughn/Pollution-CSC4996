import mongoengine

# TODO: consider adding foreign key that links Incidents collection to Articles collection

mongoengine.connect(
    db="Pollution",
    # username="root",
    # password="pollution4996",
    # authentication_source="admin",
    # host="localhost",
    # port=27017
)

class Articles(mongoengine.Document):
    url = mongoengine.StringField(required=True)
    title = mongoengine.StringField(required=True)
    publishingDate = mongoengine.StringField(required=True)

    meta = {
        'indexes': [
            {'fields': ['-url'], 'unique': True},
        ],
        'ordering': ['-publishingDate']
    }

class Urls(mongoengine.Document):
    url = mongoengine.StringField(required=True)

    meta = {
        'indexes': [
            {'fields': ['-url'], 'unique': True},
        ]
    }

class Incidents(mongoengine.Document):
    chemicals = mongoengine.ListField(mongoengine.StringField(required=True))
    date = mongoengine.StringField(required=True)
    location = mongoengine.StringField(required=True)
    officialStatement = mongoengine.StringField(required=True)
    articleLinks = mongoengine.ListField(mongoengine.StringField(required=True))