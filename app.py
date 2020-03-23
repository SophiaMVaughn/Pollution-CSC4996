from flask import Flask, render_template, redirect, url_for, request, jsonify
from flask_pymongo import PyMongo
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map
from pymongo import MongoClient
from flask_bootstrap import Bootstrap
import platform
import _json
import googlemaps
import random


print(platform.architecture())



#app = Flask(__name__)
#app.config["MONGO_URI"] = "mongodb://localhost:27017/root"
#mongo = PyMongo(app)

app = Flask(__name__)
client = MongoClient("mongodb://127.0.0.1:27017")
db = client.Pollution
collection = db.incidents

app.config['GOOGLEMAPS_KEY'] = "AIzaSyAhbiUH3iU1LV0t_IxCG0ashGNEjgNoYRI"
GoogleMaps(app)
Bootstrap(app)


def queryAllEvents():
    all_events = collection.find()
    cook = []

    #THIS LOOP IS FOR THE INCIDENT COLLECTION
    for task in all_events:
        cook.append({ 'chemicals': task['chemicals'], 'date': task['date'], 'location': task['location'], 'officialStatement': task['officialStatement'], 'articleLinks': task['articleLinks']})
    return cook

def getLocationFromCrumb(crumb):
    return crumb['location']

def convertCookieToLatLong(cookie):
    gmaps = googlemaps.Client(key="AIzaSyAhbiUH3iU1LV0t_IxCG0ashGNEjgNoYRI")#locResults= []

    locResults= []
    locations = []
    k = 0
    for crumb in cookie:
        result = gmaps.find_place( #this is the json resonse
            input=getLocationFromCrumb(crumb) + ', MI', #crumb[location] is the database query
            input_type='textquery',
            fields=['geometry'],
            location_bias='point: 42.3314, -83.0458',
            language='en'
        )
        
        locResults.append(result['candidates'])
        b = locResults[k][0].get("geometry")
        c = b.get("location")
        k += 1
        locations.append(c) #array of each lat/long
    return k, locations
    


def populate():
    cookie = queryAllEvents()
    
                #print(c)
            #print(crumb['location'])
    k, locations = convertCookieToLatLong(cookie)
    #FIGURE OUT A WAY TO TRACK LONG AND LAT TO SPECIFIC LOCATIONS TO MAKE SURE THEY ARE BEING APPLIED TO THE CORRECT LOCATIONS AS WELL AS HANDLE DUPLICATE LOCATIONS

    final = []
    d = 0
    rand = .0001
    for task in cookie:
        rand = random.uniform(.0001, .0009)
        final.append({'chemicals': task['chemicals'], 'date': task['date'], 'location': task['location'],
                        'officialStatement': task['officialStatement'], 'articleLinks': task['articleLinks'], 'lat': (locations[d].get('lat') + rand), 'lng': (locations[d].get('lng') - rand)})
        d +=1
    #for a in final:
        #print (a)
    return(final)
@app.route("/")
def home():
    populate()
    return redirect(url_for('front'))

@app.route("/home")
def front():
    return render_template('home.html')

@app.route("/TablePage", methods=['GET', 'POST'])
def table():
    cookie = populate()
    print(request.method)
    if request.method == 'POST':
        return redirect(url_for('map'))
    return render_template('TablePage.html', title = 'Table', cookie=cookie)

def addMarkerGivenEntry(entry):
    a = entry.get('chemicals')
    b = entry.get('officialStatement')
    c = entry.get('articleLinks')
    details = {
        'icon': 'http://maps.google.com/mapfiles/ms/icons/red-dot.png',
        "lat": entry.get('lat'),
        "lng": entry.get('lng'),
        "infobox": "<p><b>Date: </b>" + entry.get('date') + "</p>" +
                   "<p><b>Location: </b>" + entry.get('location') + "</p>" +
                   "<p><b>Chemicals: </b>" + ", ".join(a) + "</p>" +
                  # Taken out temporarily because sophia no likey "<p><b>Statement: </b>"  + ", ".join(b) + "</p>" +
                   "<p><b>References: </b>" + "<a href=" + ", ".join(c) +  "> Article Link</a>" + "</p>"
            }
    return details

@app.route("/MapPage", methods=['GET', 'POST'])
def map():
    final = populate()
    markers = []  # initialize a list to store your addresses
    for add in final:
        detail = addMarkerGivenEntry(add)
        markers.append(detail)



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
