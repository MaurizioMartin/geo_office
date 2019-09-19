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

@route('/static/index.css')
def send_css(filepath="/static/index.css"):
    return static_file(filepath, root='')

@route('/static/util.css')
def send_css2(filepath="/static/util.css"):
    return static_file(filepath, root='')

@route('/static/main.css')
def send_css3(filepath="/static/main.css"):
    return static_file(filepath, root='')

@route('/static/jquery-3.3.1.min.js')
def send_scr(filepath="/static/jquery-3.3.1.min.js"):
    return static_file(filepath, root='')

@route('/static/scrollify.js')
def send_scr2(filepath="/static/scrollify.js"):
    return static_file(filepath, root='')

@route('/static/jquery.scrollify.js')
def send_scr3(filepath="/static/jquery.scrollify.js"):
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

    compan_order = api.orderdf(companies_df,center)
    rests_order = api.orderdf(rests,center)
    star_order = api.orderdf(starbucks,center)

    rest_near = api.getDir(center,rests_order[["lat","lon"]].values[0])
    star_near = api.getDir(center,star_order[["lat","lon"]].values[0])
    addresscenter = api.getAddress(center)

    center_img = api.getCenterMap(center)
    companies_img = api.getMap(search,compan_order,center)
    rest_img = api.getMap(search,rests_order,center)
    starbucks_img = api.getMap(search,star_order,center)
    schools = api.getSchools(search,lat,lon)
    return template('results.html','',lat=lat,lon=lon,center_img=center_img,rest_near=rest_near,star_near=star_near,addresscenter=addresscenter,companies_img=companies_img,rest_img=rest_img,center=center,starbucks_img=starbucks_img,schools=schools,search=search,tables=[companies_df.to_html(classes='data', header="true")])

run(host='localhost', reloader=True, port=8080, debug=True)