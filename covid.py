#!/usr/bin/env python3
import requests
from datetime import date
import json
import data

WHOSITE = "https://opendata.arcgis.com/datasets/1cb306b5331945548745a5ccd290188e_2.geojson"
DATADAY = None
COVIDDATA = {}
NONDUPE = []
SORTING = {"death": [], "mortality": [], "confirmed": []}
"""
    get today's date, used to keep track of the age of current data

    Returns:
        String : todays date in ddmmyyyy format
"""


def gettoday():
    today = date.today()
    return today.strftime("%d%m%Y")


"""
    initialises a country object for the given json object

    Returns:
        Country : country object for current country with all variables entered
"""


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
    global COVIDDATA
    global NONDUPE
    global SORTING
    global DATADAY
    COVIDDATA = {}
    COUNTRYNAMES = {}
    req = requests.get(WHOSITE, allow_redirects=True)
    DATADAY = gettoday()
    NONDUPE = []
    rawcovidjson = json.loads(req.content)["features"]
    for country in rawcovidjson:
        currcountry = setcountry(country)
        names = [currcountry.name]
        if " and " in names[0]:
            names += names[0].split(" and ")
        for name in names:
            COVIDDATA[name.lower()] = currcountry
        NONDUPE.append(currcountry)
    for key in SORTING.keys():
        SORTING[key] = sorted(NONDUPE, key=lambda x: getattr(x,key), reverse=True)


def getcountry(country):
    possible = []
    if DATADAY == None or gettoday() != DATADAY:
        retrieve()
    if country.lower() in COVIDDATA.keys():
        return COVIDDATA[country].beautify()
    else:
        return False


def listcountry(number, sort):
    if DATADAY == None or gettoday() != DATADAY:
        retrieve()
    mysort = SORTING[sort]
    output = "Sorted by "+sort+"\n---------------------------\n"
    for country in mysort[:number]:
        output += country.listoutput(getattr(country,sort))
    return output

