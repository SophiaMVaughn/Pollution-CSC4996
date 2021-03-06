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

class articles(mongoengine.Document):
    url = mongoengine.StringField(required=True)
    title = mongoengine.StringField(required=True)
    publishingDate = mongoengine.StringField(required=True)

    meta = {
        'indexes': [
            {'fields': ['-url'], 'unique': True},
        ],
        'ordering': ['-publishingDate']
    }

class urls(mongoengine.Document):
    url = mongoengine.StringField(required=True)

    meta = {
        'indexes': [
            {'fields': ['-url'], 'unique': True},
        ]
    }

class incidents(mongoengine.Document):
    chemicals = mongoengine.ListField(mongoengine.StringField(required=True))
    date = mongoengine.StringField(required=True)
    location = mongoengine.StringField(required=True)
    officialStatement = mongoengine.ListField(mongoengine.StringField(required=True))
    articleLinks = mongoengine.ListField(mongoengine.StringField(required=True))

#the implementation for the errors collection (all attributes required)
#it holds all of the information that would go in the incidents collection
#along with an error message to say why it was put in the error collection
class errors(mongoengine.Document):
    chems = mongoengine.ListField(mongoengine.StringField(required=True))
    day = mongoengine.StringField(required=True)
    loc = mongoengine.StringField(required=True)
    offStmt = mongoengine.ListField(mongoengine.StringField(required=True))
    artLinks = mongoengine.ListField(mongoengine.StringField(required=True))
    errorMessage = mongoengine.StringField(required=True)
