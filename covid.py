#!/usr/bin/env python3
import requests
from datetime import date
import json
import data

WHOSITE = "https://opendata.arcgis.com/datasets/1cb306b5331945548745a5ccd290188e_2.geojson"
DATADAY = None
COVIDDATA = {}
NONDUPE = []
SORTING={"death":[],"mortality":[],"confirmed":[]}

def gettoday():
    today = date.today()
    return today.strftime("%d%m%Y")

def setcountry(country):
        properties = country["properties"]
        names = [properties["Country_Region"]]
        update = properties["Last_Update"]
        latlong = (properties["Lat"], properties["Long_"])
        confirmed = int(properties["Confirmed"])
        death = int(properties["Deaths"])
        recovered = properties["Recovered"]
        active = properties["Active"]
        incident = properties["Incident_Rate"]
        mortality = properties["Mortality_Rate"]
        currcountry = data.Country(names[0], update, latlong, confirmed, death, recovered, active,
                                   incident, mortality)
        return currcountry

def retrieve():
    global FILEDAY
    global COVIDDATA
    global NONDUPE
    COVIDDATA = {}
    COUNTRYNAMES = {}
    req = requests.get(WHOSITE, allow_redirects=True)
    DATADAY = gettoday()
    rawcovidjson = json.loads(req.content)["features"]
    for country in rawcovidjson:
        currcountry = setcountry(country)
        names = [currcountry.name]
        if " and " in names[0]:
            names += names[0].split(" and ")
        for  name in names:
            COVIDDATA[name.lower()]=currcountry
        NONDUPE.append(currcountry)

    


def getcountry(country):
    if DATADAY == None or gettoday() != DATADAY:
        retrieve()
    if country.lower() in COVIDDATA.keys():
        return COVIDDATA[country].beautify()
    else:
        return False

def listcountry(number, sort):
    clean = SORTING[sort]
    output =""
    for country in clean[:number]:
        output += country[1].listoutput(country.death)
    return output