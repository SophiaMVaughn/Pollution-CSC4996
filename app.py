from flask import Flask, render_template, redirect, url_for, request, jsonify
from flask_pymongo import PyMongo
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map
from pymongo import MongoClient
from flask_bootstrap import Bootstrap
import platform
import _json
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
    cookie.append({ 'chemicals': task['\ufeffchemicals'], 'date': task['date'], 'location': task['location'], 'officialStatement': task['officialStatement'], 'articleLinks': task['articleLinks']})

app.config['GOOGLEMAPS_KEY'] = "AIzaSyAhbiUH3iU1LV0t_IxCG0ashGNEjgNoYRI"
GoogleMaps(app)

Bootstrap(app)

gmaps = googlemaps.Client(key="AIzaSyAhbiUH3iU1LV0t_IxCG0ashGNEjgNoYRI")#locResults= []
locations = []
locResults= []
latLong = []
k = 0
for crumb in cookie:
    result = gmaps.find_place(
        input=crumb['location'] + ', MI',
        input_type='textquery',
        fields=['geometry'],
        location_bias='point: 42.3314, -83.0458',
        language='en'
    )
    locResults.append(result['candidates'])
    b = locResults[k][0].get("geometry")
    c = b.get("location")
    k += 1
    if c not in locations:
        locations.append(c)
        #print(c)
        #print(crumb['location'])

#FIGURE OUT A WAY TO TRACK LONG AND LAT TO SPECIFIC LOCATIONS TO MAKE SURE THEY ARE BEING APPLIED TO THE CORRECT LOCATIONS AS WELL AS HANDLE DUPLICATE LOCATIONS

final = []
d = 0
for task in cookie:
    final.append({'chemicals': task['chemicals'], 'date': task['date'], 'location': task['location'],
                       'officialStatement': task['officialStatement'], 'articleLinks': task['articleLinks'], 'lat': locations[d].get('lat'), 'lng': locations[d].get('lng')})
    d +=1
#for a in final:
    #print (a)
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
    markers = []  # initialize a list to store your addresses
    for add in final:
        details = {
            'icon': 'http://maps.google.com/mapfiles/ms/icons/red-dot.png',
            "lat": add.get('lat'),
            "lng": add.get('lng'),
            "infobox": add.get('location')}
        markers.append(details)



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
        markers= markers
    )
    return render_template('MapPage.html', polMap = polMap)

if __name__ == "__main__":
    app.run()