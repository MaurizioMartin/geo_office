import bottle
from bottle import route, run, post, request, static_file,template,response
import api
import data
import numpy as np
import pandas as pd


#lat = 37.7749295
#lon = -122.4194155
#radio = 2500
class EnableCors(object):
    name = 'enable_cors'
    api = 2

    def apply(self, fn, context):
        def _enable_cors(*args, **kwargs):
            # set CORS headers
            response.headers['Access-Control-Allow-Origin'] = '*'
            response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, OPTIONS'
            response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'

            if bottle.request.method != 'OPTIONS':
                # actual request; reply with the actual response
                return fn(*args, **kwargs)

        return _enable_cors


app = bottle.app()

@app.route('/cors', method=['OPTIONS', 'GET'])
def lvambience():
    response.headers['Content-type'] = 'application/json'
    return '[1]'

app.install(EnableCors())

@app.route('/')
def server_static(filepath="home.html"):
    response.set_header('Access-Control-Allow-Origin', '*')
    response.add_header('Access-Control-Allow-Methods', 'GET, POST, PUT, OPTIONS')
    return static_file(filepath, root='')

@app.route('/static/index.css')
def send_css(filepath="/static/index.css"):
    return static_file(filepath, root='')

@app.route('/static/util.css')
def send_css2(filepath="/static/util.css"):
    return static_file(filepath, root='')

@app.route('/static/main.css')
def send_css3(filepath="/static/main.css"):
    return static_file(filepath, root='')

@app.route('/static/jquery-3.3.1.min.js')
def send_scr(filepath="/static/jquery-3.3.1.min.js"):
    return static_file(filepath, root='')

@app.route('/static/scrollify.js')
def send_scr2(filepath="/static/scrollify.js"):
    return static_file(filepath, root='')

@app.route('/static/jquery.scrollify.js')
def send_scr3(filepath="/static/jquery.scrollify.js"):
    return static_file(filepath, root='')

@app.post('/doform')
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

    compan_order = data.orderdf(companies_df,center)
    rests_order = data.orderdf(rests,center)
    star_order = data.orderdf(starbucks,center)
    airport_order = data.loadDataAirports(lat,lon,center)

    rest_near = api.getDirCar(center,rests_order[["lat","lon"]].values[0])
    star_near = api.getDirWalk(center,star_order[["lat","lon"]].values[0])
    addresscenter = api.getAddress(center)

    center_img = api.getCenterMap(center)
    companies_img = api.getMap(search,compan_order,center)
    rest_img = api.getMap(search,rests_order,center)
    starbucks_img = api.getMap(search,star_order,center)
    airport_img = api.getMap(search,airport_order,center)
    schools = api.getSchools(search,lat,lon)
    return template('results.html','',lat=lat,lon=lon,airport_img=airport_img,center_img=center_img,rest_near=rest_near,star_near=star_near,addresscenter=addresscenter,companies_img=companies_img,rest_img=rest_img,center=center,starbucks_img=starbucks_img,schools=schools,search=search,tables=[compan_order.to_html(classes='data',columns=("name","description","category_code","homepage_url","distance"), header="true")],airports=[airport_order.to_html(classes='data',columns=("Airport","City","Country","distance"),header="True")])

#run(host='localhost', reloader=True, port=8080, debug=True)
app.run(port=8080)