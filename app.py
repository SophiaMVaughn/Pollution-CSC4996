from flask import Flask, render_template, redirect, url_for, request
from flask_pymongo import PyMongo
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map
from pymongo import MongoClient
from flask_bootstrap import Bootstrap
import platform
import googlemaps


print(platform.architecture())



#app = Flask(__name__)
#app.config["MONGO_URI"] = "mongodb://localhost:27017/root"
#mongo = PyMongo(app)

app = Flask(__name__)
client = MongoClient("mongodb://127.0.0.1:27017")
db = client.Pollution
collection = db.Incidents
all_events = collection.find()
cookie = []

#THIS LOOP IS FOR THE ARTICLES COLLECTION
#for task in all_events:
    #cookie.append({'articleDate': task['articleDate'], 'articleTitle': task['articleTitle'], 'url': task['url']})

#THIS LOOP IS FOR THE INCIDENT COLLECTION
for task in all_events:
    cookie.append({ 'chemicals': task['chemicals'], 'date': task['date'], 'location': task['location'], 'officialStatement': task['officialStatement'], 'articleLinks': task['articleLinks']})

app.config['GOOGLEMAPS_KEY'] = "AIzaSyAhbiUH3iU1LV0t_IxCG0ashGNEjgNoYRI"
GoogleMaps(app)

Bootstrap(app)

gmaps = googlemaps.Client(key="AIzaSyAhbiUH3iU1LV0t_IxCG0ashGNEjgNoYRI")
#locResults= []
#locations = []
#for crumb in cookie:
    #result = gmaps.find_place(
       # input=crumb['location'],
      #  input_type='textquery',
     #   fields=['place_id', 'name', 'types', 'geometry', 'formatted_address'],
    #    location_bias='point: 42.3314, -83.0458',
   #     language='en'
    #)
    #locResults.append(result)
    #for loc in locResults:
     #   print(loc)

    # https://developers.google.com/places/web-service/search#Fields
    # circle:radius@lat,lng
    # rectangle:south,west|north,east
    # https://developers.google.com/maps/faq#languagesupport

@app.route("/")
def home():
    return redirect(url_for('front'))

@app.route("/home")
def front():
    return render_template('home.html')

@app.route("/TablePage", methods=['GET', 'POST'])
def table():
    print(request.method)
    if request.method == 'POST':
        return redirect(url_for('map'))
    return render_template('TablePage.html', title = 'Table', cookie=cookie)

@app.route("/MapPage", methods=['GET', 'POST'])
def map():
    print(request.method)
    if request.method == 'POST':
        return redirect(url_for('table'))
    polMap = Map(
        identifier="fullmap",
        varname="fullmap",
        style=(
            "height:92.5%;"
            "width:100%;"
            "top:0;"
            "left:0;"
            "position:absolute;"
            "z-index:0;"
            "margin-top: 56px;"

        ),
        lat= 42.7325,
        lng= -84.5555,
        zoom = 6,
        markers=[
            {
                'icon': 'http://maps.google.com/mapfiles/ms/icons/red-dot.png',
                'lat': 45.87556,
                'lng': -84.73229,
                'infobox': "St. Ignace"
            },
            {
                'icon': 'http://maps.google.com/mapfiles/ms/icons/red-dot.png',
                'lat': 43.80195,
                'lng': -83.00077,
                'infobox': "Bad Axe"
            },
            {
                'icon': 'http://maps.google.com/mapfiles/ms/icons/red-dot.png',
                'lat': 41.89754,
                'lng': -84.03716,
                'infobox': "Adrian"
            },
            {
                'icon': 'http://maps.google.com/mapfiles/ms/icons/red-dot.png',
                'lat': 46.49771,
                'lng': -84.34758,
                'infobox': "Sault Ste. Marie"
            },
            {
                'icon': 'http://maps.google.com/mapfiles/ms/icons/red-dot.png',
                'lat': 45.64695,
                'lng': -84.47447,
                'infobox': "Cheyboygan"
            },
            {
                'icon': 'http://maps.google.com/mapfiles/ms/icons/red-dot.png',
                'lat': 41.94032,
                'lng': -85.00052,
                'infobox': "Coldwater"
            },
            {
                'icon': 'http://maps.google.com/mapfiles/ms/icons/red-dot.png',
                'lat': 41.92004,
                'lng': -84.63051,
                'infobox': "Hillsdale"
            },
            {
                'icon': 'http://maps.google.com/mapfiles/ms/icons/red-dot.png',
                'lat': 42.98725,
                'lng': -85.07111,
                'infobox': '<h2>Coldwater</h2>'+
                '<p>This is the map pin for Coldwater</p>'+
                '<img src="static/img/pollution1.png">'+
                '<a href="https://www.coldwater.org">Coldwater Link</a>'
            },
            {
                'icon': 'http://maps.google.com/mapfiles/ms/icons/red-dot.png',
                'lat': 42.3314,
                'lng': -83.0458,
                'infobox': "Detroit"
            }
        ]
    )
    return render_template('MapPage.html', polMap = polMap)

if __name__ == "__main__":
    app.run()