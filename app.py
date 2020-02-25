from flask import Flask, render_template, redirect, url_for, request
from flask_pymongo import PyMongo
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map
from pymongo import MongoClient
from flask_bootstrap import Bootstrap
import platform

print(platform.architecture())



#app = Flask(__name__)
#app.config["MONGO_URI"] = "mongodb://localhost:27017/root"
#mongo = PyMongo(app)

app = Flask(__name__)
client = MongoClient("mongodb://127.0.0.1:27017")
db = client.Pollution
collection = db.incidents
all_events = collection.find()
cookie = []
for task in all_events:
    cookie.append({'articleDate': task['articleDate'], 'articleTitle': task['articleTitle'], 'url': task['url']})

app.config['GOOGLEMAPS_KEY'] = "AIzaSyAhbiUH3iU1LV0t_IxCG0ashGNEjgNoYRI"
GoogleMaps(app)

Bootstrap(app)

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
            "height:100%;"
            "width:100%;"
            "top:0;"
            "left:0;"
            "position:absolute;"
            "z-index:0;"
            "margin-top: 56px;"
        ),
        lat= 42.7325,
        lng= -84.5555,
        zoom = 6
    )
    return render_template('MapPage.html', polMap = polMap)

if __name__ == "__main__":
    app.run()