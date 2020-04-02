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
from datetime import datetime


print(platform.architecture())



#app = Flask(__name__)
#app.config["MONGO_URI"] = "mongodb://localhost:27017/root"
#mongo = PyMongo(app)

app = Flask(__name__)
client = MongoClient("mongodb://127.0.0.1:27017")
db = client.Pollution
collection = db.incidents
errorColl = db.errors

app.config['GOOGLEMAPS_KEY'] = "AIzaSyAhbiUH3iU1LV0t_IxCG0ashGNEjgNoYRI"
GoogleMaps(app)
Bootstrap(app)


def populate():

    all_events = collection.find()
    cookie = []

#THIS LOOP IS FOR THE ARTICLES COLLECTION
#for task in all_events:
    #cookie.append({'articleDate': task['articleDate'], 'articleTitle': task['articleTitle'], 'url': task['url']})

#THIS LOOP IS FOR THE INCIDENT COLLECTION
    for task in all_events:
        #print(task)
        cookie.append({ 'chemicals': task['chemicals'], 'date': task['date'], 'location': task['location'], 'officialStatement': task['officialStatement'], 'articleLinks': task['articleLinks']})



    gmaps = googlemaps.Client(key="AIzaSyAhbiUH3iU1LV0t_IxCG0ashGNEjgNoYRI")#locResults= []
    locations = []
    locResults= []
    k = 0
    for crumb in cookie:
        result = gmaps.find_place(
            input=crumb['location'] + ', MI',
            input_type='textquery',
            fields=['geometry'],
            location_bias='point: 42.3314, -83.0458',
            language='en'
        )
##        if crumb['location']=="Lake Huron":
##            print(result)
        if result['candidates']:
            #print(result['candidates'][0].get("geometry").get("location"))
            locResults.append(result['candidates'])
            b = locResults[k][0].get("geometry")
            c = b.get("location")
            k += 1
            locations.append(c)
        else:
            mapTemp = crumb
            cookie.remove(crumb)
            mapTempErr = {'chems': mapTemp.get('chemicals'), 'day': mapTemp.get('date'), 'loc': mapTemp.get('location'),'offStmt': mapTemp.get('officialStatement'), 'artLinks': mapTemp.get('articleLinks')}
            mapTempErr['errorMessage'] = "The location could not be found with google"
            x = errorColl.insert_one(mapTempErr)
            collection.delete_one(mapTemp)


    #FIGURE OUT A WAY TO TRACK LONG AND LAT TO SPECIFIC LOCATIONS TO MAKE SURE THEY ARE BEING APPLIED TO THE CORRECT LOCATIONS AS WELL AS HANDLE DUPLICATE LOCATIONS

    final = []
    d = 0
    rand = .0001
    for task in cookie:
        rand = random.uniform(.0001, .0009)
        lakeHuron = random.uniform(-.05, .05)
        try:
            if locations[d].get('lat')==45.0521793 and locations[d].get('lng')==-82.48509399999999:
                modif = 0
                if d%2==1:
                    modif = -1
                else:
                    modif = 1
                final.append({'chemicals': task['chemicals'], 'date': task['date'], 'location': "Could not find a specific MI location",
                        'officialStatement': task['officialStatement'], 'articleLinks': task['articleLinks'], 'lat': (locations[d].get('lat') - (modif*lakeHuron)), 'lng': (locations[d].get('lng') + (modif*lakeHuron))})
                print("default location for item "+str(d))
            else:
                final.append({'chemicals': task['chemicals'], 'date': task['date'], 'location': task['location'],
                        'officialStatement': task['officialStatement'], 'articleLinks': task['articleLinks'], 'lat': (locations[d].get('lat') + rand), 'lng': (locations[d].get('lng') - rand)})
            d +=1
        except:
            continue
    #for a in final:
        #print (a)
    for item in final:
        if (len(item.get('date'))==0) or (item.get('lat') < 41.695368) or (item.get('lat') > 47.480572 ) or (item.get('lng') < -90.414226) or (item.get('lng') > -82.418457) or (item.get('lng') < -87.637561 and item.get('lat') < 45.318741):
            temp = item
            final.remove(item)
            dbTempDel = {'chemicals': temp.get('chemicals'), 'date': temp.get('date'), 'location': temp.get('location'), 'officialStatement': temp.get('officialStatement'), 'articleLinks': temp.get('articleLinks')}
            dbTemp = {'chems': temp.get('chemicals'), 'day': temp.get('date'), 'loc': temp.get('location'), 'offStmt': temp.get('officialStatement'), 'artLinks': temp.get('articleLinks')}
            dbTemp['errorMessage'] = "The location fell outside of the boundaries of Michigan or there was no day"
            x = errorColl.insert_one(dbTemp)
            collection.delete_one(dbTempDel)
            print("Error object sent to Errors collection, object ID below: ")
            print(x)
        else:
            date = item.get('date')
            try:
                date = datetime.strptime(date, '%m/%d/%Y')
            except:
                tempDate = item
                final.remove(item)
                dbTempDateDel = {'chemicals': tempDate.get('chemicals'), 'date': tempDate.get('date'), 'location': tempDate.get('location'), 'officialStatement': tempDate.get('officialStatement'), 'articleLinks': tempDate.get('articleLinks')}
                dbTempDate = {'chems': tempDate.get('chemicals'), 'day': tempDate.get('date'), 'loc': tempDate.get('location'), 'offStmt': tempDate.get('officialStatement'), 'artLinks': tempDate.get('articleLinks')}
                dbTempDate['errorMessage'] = "Invalid Date"
                x = errorColl.insert_one(dbTempDate)
                collection.delete_one(dbTempDateDel)
    return(final)

#filtered date function complete now do a sorted date function
def filterDate(a, b):
    #check date formatting
    try:
        c = datetime.strptime(a, '%m/%d/%Y')
        d = datetime.strptime(b, '%m/%d/%Y')
    except ValueError:
        c = datetime.strptime('01/01/2000', '%m/%d/%Y')
        d = datetime.strptime('12/30/2020', '%m/%d/%Y')
    print(c)
    print(d)
    dateArray = []
    preArray = populate()
    for item in preArray:
        date = item.get('date')
        date = datetime.strptime(date, '%m/%d/%Y')
        if (c < date < d):
            dateArray.append(item)
    return(dateArray)

def sortDates():
    dateArray = []
    preArray = populate()
    dateArray = sorted(preArray, key=lambda x: datetime.strptime(x['date'], '%m/%d/%Y'), reverse=True)
    return(dateArray)

def grabChemical(a, b):
    chemArray = []
    for item in b:
        for chem in item.get('chemicals'):
            if chem.lower() == a.lower():
                chemArray.append(item)
    return(chemArray)


@app.route("/")
def home():
    return redirect(url_for('front'))

@app.route("/home")
def front():
    load = populate()
    return render_template('home.html')

@app.route("/TablePage", methods=['GET', 'POST'])
def table():
    cookie = sortDates()
    print(request.method)
    #if request.method == 'POST':
        #return redirect(url_for('map'))
    return render_template('TablePage.html', title = 'Table', cookie=cookie)

@app.route("/FilteredTablePage", methods=['GET', 'POST'])
def filteredTable():
    cookie = sortDates()
    if(request.args['chemSearch'] != None):
        a = request.args['chemSearch']
        cookie = grabChemical(a, cookie)
    print(request.method)
    return render_template('TablePage.html', title = 'Table', cookie=cookie)


@app.route("/MapPage", methods=['GET', 'POST'])
def map():
    #call a new function that grabs final array and only gets dates within specific range
    final = populate()
    markers = []  # initialize a list to store your addresses
    for add in final:
        a = add.get('chemicals')
        b = add.get('officialStatement')
        c = add.get('articleLinks')
        details = {
            'icon': 'http://maps.google.com/mapfiles/ms/icons/red-dot.png',
            "lat": add.get('lat'),
            "lng": add.get('lng'),
            "infobox": "<p><b>Date: </b>" + add.get('date') + "</p>" +
                       "<p><b>Location: </b>" + add.get('location') + "</p>" +
                       "<p><b>Chemicals: </b>" + ", ".join(a) + "</p>" +
                      # Taken out temporarily because sophia no likey "<p><b>Statement: </b>"  + ", ".join(b) + "</p>" +
                       "<p><b>References: </b>" + "<a href=" + ", ".join(c) +  "> Article Link</a>" + "</p>"
                }
        markers.append(details)



    print(request.method)
    #if request.method == 'POST':
        #return redirect(url_for('table'))
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

@app.route("/FilteredMapPage", methods=['GET', 'POST'])
def filteredMap():
    #call a new function that grabs final array and only gets dates within specific range
    final = populate()
    if(request.args['startDate'] != None):
        a = request.args['startDate']
        b = request.args['endDate']
        final = filterDate(a,b)


    markers = []  # initialize a list to store your addresses
    for add in final:
        a = add.get('chemicals')
        b = add.get('officialStatement')
        c = add.get('articleLinks')
        details = {
            'icon': 'http://maps.google.com/mapfiles/ms/icons/red-dot.png',
            "lat": add.get('lat'),
            "lng": add.get('lng'),
            "infobox": "<p><b>Date: </b>" + add.get('date') + "</p>" +
                       "<p><b>Location: </b>" + add.get('location') + "</p>" +
                       "<p><b>Chemicals: </b>" + ", ".join(a) + "</p>" +
                      # Taken out temporarily because sophia no likey "<p><b>Statement: </b>"  + ", ".join(b) + "</p>" +
                       "<p><b>References: </b>" + "<a href=" + ", ".join(c) +  "> Article Link</a>" + "</p>"
                }
        markers.append(details)



    print(request.method)
    #if request.method == 'POST':
        #return redirect(url_for('table'))
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
