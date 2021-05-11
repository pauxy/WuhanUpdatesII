#!/usr/bin/env python3
import requests
from datetime import date
import json

WHOSITE = "https://opendata.arcgis.com/datasets/1cb306b5331945548745a5ccd290188e_2.geojson"
FILEDAY = None
COVIDDATA = None


def gettoday():
    today = date.today()
    return today.strftime("%d%m%Y")


def retrieve():
    global FILEDAY
    global COVIDDATA
    req = requests.get(WHOSITE, allow_redirects=True)
    FILEDAY = gettoday()
    rawcovidjson = json.loads(req.content)
    COVIDDATA = rawcovidjson["features"]


def getcountry(country):
    if FILEDAY == None or gettoday() != FILEDAY:
        retrieve()
    for country in COVIDDATA:
        print(country["properties"])


print(getcountry("SG"))
