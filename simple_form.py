from bottle import route, run, post, request, static_file,template
import api
import data
import numpy as np
import pandas as pd

#lat = 37.7749295
#lon = -122.4194155
#radio = 2500

@route('/')
def server_static(filepath="home.html"):
    return static_file(filepath, root='')

@post('/doform')
def process():
    search = request.forms.get('searchbox')
    geo = api.getGeoloc(search)
    lat = geo["lat"]
    lon = geo["lng"]
    radio = 2500
    companies_df = data.getDf(lat,lon,radio)
    zomatodict = api.getZomatoCityID(search)
    rests = api.getVeganRestaurants(zomatodict["id"])
    starbucks = api.getStarbucks(zomatodict["id"])

    center_companies = api.getCenter(companies_df)
    center_rests = api.getCenter(rests)
    center_starbucks = api.getCenter(starbucks)
    center = api.getCenterPonderate(center_companies,center_rests,center_starbucks)

    companies_img = api.getMap(search,companies_df,center)
    rest_img = api.getMap(search,rests,center)
    starbucks_img = api.getMap(search,starbucks,center)
    schools = api.getSchools(search,lat,lon)
    return template('results.html','',lat=lat,lon=lon,companies_img=companies_img,rest_img=rest_img,center=center,starbucks_img=starbucks_img,schools=schools,search=search,tables=[companies_df.to_html(classes='data', header="true")])

run(host='localhost', reloader=True, port=8080, debug=True)