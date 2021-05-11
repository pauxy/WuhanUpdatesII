#!/usr/bin/env python3
import requests
from datetime import date
import json
import data

WHOSITE = "https://opendata.arcgis.com/datasets/1cb306b5331945548745a5ccd290188e_2.geojson"
FILEDAY = None
COVIDDATA = {}


def gettoday():
    today = date.today()
    return today.strftime("%d%m%Y")


def retrieve():
    global FILEDAY
    global COVIDDATA
    COVIDDATA = {}
    req = requests.get(WHOSITE, allow_redirects=True)
    FILEDAY = gettoday()
    rawcovidjson = json.loads(req.content)["features"]
    for country in rawcovidjson:
        properties = country["properties"]
        name = properties["Country_Region"]
        update = properties["Last_Update"]
        latlong = (properties["Lat"], properties["Long_"])
        confirmed = properties["Confirmed"]
        death = properties["Deaths"]
        recovered = properties["Recovered"]
        active = properties["Active"]
        incident = properties["Incident_Rate"]
        mortality = properties["Mortality_Rate"]
        currcountry = data.Country(name, update, latlong, confirmed, death, recovered, active,
                                   incident, mortality)
        COVIDDATA[name] = currcountry


def getcountry(country):
    if FILEDAY == None or gettoday() != FILEDAY:
        retrieve()
    return COVIDDATA[country].beautify()
