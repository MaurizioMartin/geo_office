#https://maps.googleapis.com/maps/api/geocode/json?address=1600+Amphitheatre+Parkway,
#+Mountain+View,+CA&key=YOUR_API_KEY

import os
import requests
from dotenv import load_dotenv
from urllib.parse import urlencode
from bs4 import BeautifulSoup
import pandas as pd
import urllib.request
from uber_rides.session import Session
from uber_rides.client import UberRidesClient
load_dotenv()

GOOGLE_CRED = os.getenv("GOOGLE_CRED")
ZOMATO_CRED = os.getenv("ZOMATO_CRED")
UBER_CRED = os.getenv("UBER_CRED")
UBER_ACCESS_TOKEN = os.getenv("UBER_ACCESS_TOKEN")

def getGeoloc(params):
    params = "address="+params
    url = "https://maps.googleapis.com/maps/api/geocode/json?{}&key={}".format(params,GOOGLE_CRED)
    response = requests.get(url)
    data = response.json()
    for dat in data["results"]:
        return dat["geometry"]["location"]

def getZomatoCityID(params):
    headers = {    
       "user-key": "{}".format(ZOMATO_CRED)
    }
    params = "q="+params
    url = "https://developers.zomato.com/api/v2.1/cities?{}".format(params)
    response = requests.get(url,headers=headers)
    data=response.json()
    dat = data["location_suggestions"]
    zomato_dict={
    "id":dat[0]["id"],
    "name":dat[0]["name"],
    "country_id": dat[0]["country_id"],
    "country_name": dat[0]["country_name"],
    "state_id": dat[0]["state_id"],
    "state_name": dat[0]["state_name"]
    }
    return zomato_dict

def getVeganRestaurants(id):
    headers = {    
       "user-key": "{}".format(ZOMATO_CRED)
    }
    url="https://developers.zomato.com/api/v2.1/search?entity_id="+str(id)+"&entity_type=city&count=10&radius=3000&cuisines=308&sort=rating&order=desc"
    response = requests.get(url,headers=headers)
    data=response.json()
    #print(data)
    zomato_list=[]
    for restaurant in data["restaurants"]:
        zomato_dict = {
            "rest_id": restaurant["restaurant"]["id"],
            "rest_name": restaurant["restaurant"]["name"],
            "address": restaurant["restaurant"]["location"]["address"],
            "lat": restaurant["restaurant"]["location"]["latitude"],
            "lon": restaurant["restaurant"]["location"]["longitude"]
        }
        zomato_list.append(zomato_dict)

    rests_df = pd.DataFrame(zomato_list)


    return rests_df

def getStarbucks(id):    
    headers = {    
       "user-key": "{}".format(ZOMATO_CRED)
    }
    url="https://developers.zomato.com/api/v2.1/search?entity_id="+str(id)+"&entity_type=city&q=starbucks&count=10&radius=1000"
    response = requests.get(url,headers=headers)
    data=response.json()
    zomato_list=[]
    for restaurant in data["restaurants"]:
        zomato_dict = {
            "rest_id": restaurant["restaurant"]["id"],
            "rest_name": restaurant["restaurant"]["name"],
            "address": restaurant["restaurant"]["location"]["address"],
            "lat": restaurant["restaurant"]["location"]["latitude"],
            "lon": restaurant["restaurant"]["location"]["longitude"]
        }
        zomato_list.append(zomato_dict)
    starbucks_df = pd.DataFrame(zomato_list)
    return starbucks_df

def getCenter(df1):
    suma = 0
    medlat = 0
    medlon = 0
    for col in df1[["lat","lon"]].values:
        suma+=1
        medlat+=float(col[0])
        medlon+=float(col[1])
    return [medlat/suma,medlon/suma]

def getCenterPonderate(com,res,star):
    lat = (com[0]*0.3)+(res[0]*0.2)+(star[0]*0.5)
    lon = (com[1]*0.3)+(res[1]*0.2)+(star[1]*0.5)
    return [lat,lon]

def getAddress(center):
    url = "https://maps.googleapis.com/maps/api/geocode/json?latlng="+str(center[0])+","+str(center[1])+"&key="+GOOGLE_CRED
    response = requests.get(url)
    data=response.json()
    data=data["results"][0]["formatted_address"]
    return data


def getMap(search,df,center):
    marcadores=[]
    label = 0

    for col in df[["lat","lon"]].values:
        marcadores.append("&markers=color:blue%7Clabel:"+str(label)+"%7C"+str(col[0])+","+str(col[1]))
        label+=1
    marcadores.append("&markers=color:red%7Clabel:C%7C"+str(center[0])+","+str(center[1]))
    marcadores= "".join(marcadores)
    #print(marcadores)
    #img = "https://maps.googleapis.com/maps/api/staticmap?center="+search+"&zoom=13&size=600x300&maptype=roadmap&markers=color:blue%7Clabel:S%7C"+str(lat)+","+str(lon)+"&key="+GOOGLE_CRED
    img = "https://maps.googleapis.com/maps/api/staticmap?center="+search+"&zoom=13&size=600x450&maptype=roadmap"+marcadores+"&key="+GOOGLE_CRED
    return img

def getSchools(search,lat,lon):
    src="https://www.google.com/maps/embed/v1/search?key="+GOOGLE_CRED+"&q=schools+in+"+search+"&zoom=12&center="+str(lat)+","+str(lon)
    return src

def getCenterMap(center):
    src="https://www.google.com/maps/embed/v1/view?key="+GOOGLE_CRED+"&center="+str(center[0])+","+str(center[1])+"&zoom=18&maptype=satellite"
    return src

def getDirWalk(center,coord):
    orig=getAddress(center)
    orig=orig.replace(" ","+")
    dest=getAddress(coord)
    dest=dest.replace(" ","+")
    src="https://www.google.com/maps/embed/v1/directions?key="+GOOGLE_CRED+"&origin="+orig+"&destination="+dest+"&mode=walking"
    return src

def getDirCar(center,coord):
    orig=getAddress(center)
    orig=orig.replace(" ","+")
    dest=getAddress(coord)
    dest=dest.replace(" ","+")
    src="https://www.google.com/maps/embed/v1/directions?key="+GOOGLE_CRED+"&origin="+orig+"&destination="+dest+"&mode=driving"
    return src

def autocomplete():
    url = "https://maps.googleapis.com/maps/api/place/autocomplete/json?input=Vict&types=geocode&key={}".format(GOOGLE_CRED)
    response = requests.get(url)
    data=response.json()
    return data

def uberSession():
    session = Session(server_token=UBER_CRED)
    client = UberRidesClient(session)
    print(client)
    return client

def getPrices():
    headers = {    
       "Authorization": "Bearer {}".format(UBER_ACCESS_TOKEN)
    }
    url = 'https://api.uber.com/v1.2/estimates/price?start_latitude=37.7752315&start_longitude=-122.418075&end_latitude=37.7752415&end_longitude=-122.518075'
    response = requests.get(url,headers=headers)
    print(response.status_code)
    data=response.json()
    return data

