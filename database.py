import mongoengine

mongoengine.connect(
    db="Pollution",
    # username="root",
    # password="pollution4996",
    # authentication_source="admin",
    # host="localhost",
    # port=27017
)

class Articles(mongoengine.Document):
    publishingDate = mongoengine.StringField(required=True)
    title = mongoengine.StringField(required=True)
    url = mongoengine.StringField(required=True)

    meta = {
        'indexes': [
            {'fields': ['-url'], 'unique': True},
        ],
        'ordering': ['-articleDate']
    }