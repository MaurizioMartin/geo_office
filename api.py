#https://maps.googleapis.com/maps/api/geocode/json?address=1600+Amphitheatre+Parkway,
#+Mountain+View,+CA&key=YOUR_API_KEY

import os
import requests
from dotenv import load_dotenv
from urllib.parse import urlencode
from bs4 import BeautifulSoup
import urllib.request
load_dotenv()

GOOGLE_CRED = os.getenv("GOOGLE_CRED")
ZOMATO_CRED = os.getenv("ZOMATO_CRED")

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

def getZomatoRestaurants():
    headers = {    
       "user-key": "{}".format(ZOMATO_CRED)
    }
    url="https://developers.zomato.com/api/v2.1/search?entity_id=10847&entity_type=city&radius=3000&cuisines=308"
    response = requests.get(url,headers=headers)
    return response.json()

if __name__=='__main__':
    test = input("Localizacion: ")
    print(test)
    print(getGeoloc(test))
    #print(getZomatoCityID(test))
    