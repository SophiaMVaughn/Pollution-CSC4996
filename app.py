from flask import Flask, render_template, redirect, url_for, request
from flask_pymongo import PyMongo

from pymongo import MongoClient
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

@app.route("/")
def home():
    return redirect(url_for('table'))

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
    return render_template('MapPage.html')

if __name__ == "__main__":
    app.run()