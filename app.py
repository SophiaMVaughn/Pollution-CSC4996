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


#here is where I establish the database and collection
app = Flask(__name__)
client = MongoClient("mongodb://127.0.0.1:27017")
db = client.Pollution
collection = db.incidents
errorColl = db.errors

#this is the google maps api key
app.config['GOOGLEMAPS_KEY'] = "AIzaSyAhbiUH3iU1LV0t_IxCG0ashGNEjgNoYRI"
GoogleMaps(app)
Bootstrap(app)

totalCount = 0
def populate():

    all_events = collection.find()
    cookie = []
    global totalCount
    totalCount = 0
#I loop through all_events which grabbed the data from the incidents collection, and am putting them into an array
    for task in all_events:
        #print(task)
        cookie.append({ 'chemicals': task['chemicals'], 'date': task['date'], 'location': task['location'], 'officialStatement': task['officialStatement'], 'articleLinks': task['articleLinks']})

    gmaps = googlemaps.Client(key="AIzaSyAhbiUH3iU1LV0t_IxCG0ashGNEjgNoYRI")#locResults= []
    locations = []
    locResults= []
    k = 0
    #we use the google places api to get the lat and long for a location so we are looping through the array and calling find_place on every location
    for crumb in cookie:
        if crumb['location'] != "none":
            result = gmaps.find_place(
                input=crumb['location'] + ', MI',
                input_type='textquery',
                fields=['geometry'],
                location_bias='point: 42.3314, -83.0458',
                language='en'
            )
##        if crumb['location']=="Lake Huron":
##            print(result)
        #the find_place returns a json response and below is me parsing through it to get the lat and long since thats all we want out of the response
            if result['candidates']:
                #print(result['candidates'][0].get("geometry").get("location"))
                locResults.append(result['candidates'])
                b = locResults[k][0].get("geometry")
                c = b.get("location")
                k += 1
                locations.append(c)
        #some locations even google can find so this will catch them and send them to the error database
            else:
                mapTemp = crumb
                cookie.remove(crumb)
                mapTempErr = {'chems': mapTemp.get('chemicals'), 'day': mapTemp.get('date'), 'loc': mapTemp.get('location'),'offStmt': mapTemp.get('officialStatement'), 'artLinks': mapTemp.get('articleLinks')}
                mapTempErr['errorMessage'] = "The location could not be found with google"
                x = errorColl.insert_one(mapTempErr)
                collection.delete_one(mapTemp)
        else:
            lakeHuron = random.uniform(-.05, .05)
            locations.append({'lat': 44.765522  - lakeHuron, 'lng': -82.817534 + lakeHuron})
            crumb['location'] = "Could not find a specific MI location"

    final = []
    d = 0
    rand = .0001
    #below we are adding each locations lat and long to the overall stored event, we also add slight variance so the pins for the same locations aren't on top of each other
    for task in cookie:
        rand = random.uniform(.0001, .0009)
        final.append({'chemicals': task['chemicals'], 'date': task['date'], 'location': task['location'],
                        'officialStatement': task['officialStatement'], 'articleLinks': task['articleLinks'], 'lat': (locations[d].get('lat') + rand), 'lng': (locations[d].get('lng') - rand)})
        d +=1
        totalCount += 1
    #for a in final:
        #print (a)
    #this will catch any location outside of michigan or if there is a blank date and send them to the error database
    for item in final:
        if (item.get('date')=="") or (item.get('lat') < 41.695368) or (item.get('lat') > 47.480572 ) or (item.get('lng') < -90.414226) or (item.get('lng') > -82.418457) or (item.get('lng') < -87.637561 and item.get('lat') < 45.318741):
            temp = item
            try:
                final.remove(item)
                totalCount = totalCount - 1
            except ValueError:
                continue
            dbTempDel = {'chemicals': temp.get('chemicals'), 'date': temp.get('date'), 'officialStatement': temp.get('officialStatement'), 'articleLinks': temp.get('articleLinks')}
            dbTemp = {'chems': temp.get('chemicals'), 'day': temp.get('date'), 'loc': temp.get('location'), 'offStmt': temp.get('officialStatement'), 'artLinks': temp.get('articleLinks')}
            dbTemp['errorMessage'] = "The location fell outside of the boundaries of Michigan or there was no day"
            x = errorColl.insert_one(dbTemp)
            collection.delete_one(dbTempDel)
            print("Error object sent to Errors collection, object ID below: ")
            print(x)
    return(final)

#calling the initial populate function from before the user even enters the page so it'll do all of the heavy lifting the second the web application runs on the server
initial = []
def call_pop():
    global initial
    initial = populate()
call_pop()

#A jerryrigged trigger to check if the database has been updated
def check_for_new():
    check_events = collection.find()
    localCount = 0
    for task in check_events:
        localCount += 1
    print(totalCount)
    print(localCount)
    if localCount != totalCount:
        call_pop()

#this function is called when filtering between 2 dates on the map page, it takes the dates and formats them correctly then returns an array of every event with dates in between
def filterDate(a, b):
    #check date formatting
    c = datetime.strptime(a, '%m/%d/%Y')
    d = datetime.strptime(b, '%m/%d/%Y')
    print(c)
    print(d)
    dateArray = []
    preArray = initial
    for item in preArray:
        date = item.get('date')
        date = datetime.strptime(date, '%m/%d/%Y')
        if (c < date < d):
            dateArray.append(item)
    return(dateArray)
#this function is called whenever you load the table page and will sort the dates from newest to oldest
def sortDates():
    dateArray = []
    preArray = initial
    dateArray = sorted(preArray, key=lambda x: datetime.strptime(x['date'], '%m/%d/%Y'), reverse=True)
    return(dateArray)
#this function is called whenever a chemical is searched on the table page and return any event with a chemical matching the one searched
def grabChemical(a, b):
    chemArray = []
    for item in b:
        for chem in item.get('chemicals'):
            if chem.lower() == a.lower():
                chemArray.append(item)
    return(chemArray)

#this is the initial route when loading the web app and it will reroute to the home page
@app.route("/")
def home():
    return redirect(url_for('front'))
#this will render the home page html
@app.route("/home")
def front():
    check_for_new()
    return render_template('home.html')
#this will render the aboutus html
@app.route("/AboutUs")
def about():
    return render_template('AboutUs.html')
#this is for the table page and before rendering the page it will sort the dates and render the html with the array so it can be displayed
@app.route("/TablePage", methods=['GET', 'POST'])
def table():
    cookie = sortDates()
    print(request.method)
    #if request.method == 'POST':
        #return redirect(url_for('map'))
    return render_template('TablePage.html', title = 'Table', cookie=cookie)
#this is routed to when the user searches a specific chemical and will take the request arg and build a new array to render with the html that's only events returned by grabChemical
@app.route("/FilteredTablePage", methods=['GET', 'POST'])
def filteredTable():
    cookie = sortDates()
    if(request.args['chemSearch'] != None):
        a = request.args['chemSearch']
        cookie = grabChemical(a, cookie)
    print(request.method)
    return render_template('TablePage.html', title = 'Table', cookie=cookie)

#this is the map page route and before rendering the page I mimicked html in python to dynamically generate pins for each of the events in the array so you are able to generate them in the app.py instead of the html so you don't need to carry the array over
@app.route("/MapPage", methods=['GET', 'POST'])
def map():
    #call a new function that grabs final array and only gets dates within specific range
    final = initial
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

    #I'm also creating the map here too
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
#this route is for the filtered map, so dates only within the range the user searched
@app.route("/FilteredMapPage", methods=['GET', 'POST'])
def filteredMap():
    #call a new function that grabs final array and only gets dates within specific range
    final = initial
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
#this will run the app
if __name__ == "__main__":
    app.run()
