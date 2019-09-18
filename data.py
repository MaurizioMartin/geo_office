from pymongo import MongoClient
import pandas as pd
import json
    

def conections(host="localhost",port="27017"):
    client = MongoClient("mongodb://"+host+":"+port+"/")
    db = client.companies
    return db

def loadData(db):
    data = db.companiesfil.find()
    df = pd.DataFrame(data)
    return df

def geonear(db, geopoint, maxdistance=1000):
    data = db.companiesfil.find({
        "geo":{
            "$near":{
                "$geometry":geopoint,
                "$maxDistance":maxdistance
            }}})
    df = pd.DataFrame(data)
    return df


def geopoint(lat,lon):
    return {'type': 'Point', 'coordinates': [lon, lat]}

def getlat(geopoint):
    lat = geopoint["coordinates"][1]
    return lat

def getlon(geopoint):
    lon = geopoint["coordinates"][0]
    return lon

def getDf(lat,lon,radio):
    db = conections()
    geo = geopoint(lat,lon)
    df = geonear(db,geo,radio)
    df["lat"] = df["geo"].apply(getlat)
    df["lon"] = df["geo"].apply(getlon)
    df = df[["name","description","category_code","homepage_url","lat","lon"]]
    return df

