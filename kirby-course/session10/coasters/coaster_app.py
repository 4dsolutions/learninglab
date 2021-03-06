# -*- coding: utf-8 -*-
"""
Created on Thu Feb 16 16:05:10 2017

@author: kurner
"""

from make_coasters_db import DB
from flask import Flask, Response, request
from jinja2 import Environment, PackageLoader
import sys
import json

sys.path.append("/Users/kurner/Downloads/session10/")

app = Flask(__name__)

env = Environment(
    loader=PackageLoader('coasters', 'templates'),
)

@app.route("/")
def index():
    template = env.get_template('home.html')
    return template.render()

@app.route("/coasters")
def coasters():
    the_data = all_coasters()
    template = env.get_template('coaster_listing.html')
    return template.render(coasters= the_data)

@app.route("/coaster/<coaster>", methods=["POST", "GET"])
def coaster(coaster):
    if request.method == "POST":
        print("POST DATA")

    the_data = one_coaster(coaster)
    template = env.get_template('coaster.html')
    return template.render(the_data = the_data[0])

@app.route("/api/coaster/<coaster>")
def json_coaster(coaster):
    the_data = one_coaster(coaster)
    json_string = json.dumps(the_data[0])
    return Response(response=json_string, status=200, mimetype = "application/json")

@app.route("/update/<coaster>")
def edit_coaster(coaster):
    the_data = one_coaster(coaster)
    print(the_data[0][1])
    template = env.get_template('update_coaster.html')
    return template.render(the_data = the_data[0])

def all_coasters():
    with DB() as db:
        query = ("SELECT name, park, yr_opened FROM Coasters "
                 "ORDER BY name")
        db.get_coasters(query)
        return tuple(db.cursor.fetchall())

def one_coaster(coaster):
    with DB() as db:
        if "'" in coaster:
            coaster = coaster.replace("'", "''")
        if "," in coaster:
            coaster = coaster.replace(",", "%")
            coaster=coaster[:coaster.index('%')+1]
        if "%" not in coaster:
            query = ("SELECT * FROM Coasters "
                     "WHERE name = '{}'".format(coaster))
        else:
            query = ("SELECT * FROM Coasters "
                     "WHERE name LIKE '{}'".format(coaster))            
        print("Seeking: ", query)
        db.get_coasters(query)
        return db.cursor.fetchall()

        
if __name__ == "__main__":
    app.run()
    