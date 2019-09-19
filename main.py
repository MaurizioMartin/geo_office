import api
import data
import pandas as pd


# Algunas coordenadas de interés
# fifth_avenue = {'type': 'Point', 'coordinates': [-73.9678246, 40.7744089]}
# mountain_view = {'type': 'Point', 'coordinates': [-122.086419, 37.387120]}
# microsoft = {'type': 'Point', 'coordinates': [-122.071367, 37.412692]}
# san_francisco = {'type': 'Point', 'coordinates': [-122.4194155, 37.7749295]}

if __name__=='__main__':
    '''
    test = input("Localizacion: ")
    print(test)
    print(api.getGeoloc(test))
    zomatodict = api.getZomatoCityID(test)
    rests = api.getVeganRestaurants(zomatodict["id"])
    starbucks = api.getStarbucks(zomatodict["id"])
    print(zomatodict)
    print(rests)
    print(starbucks)
    
    db = data.conections()
    geo = data.geopoint(37.7749295,-122.4194155)
    df = data.geonear(db,geo,2500)
    print(df)
    '''
    lat = 37.7749295
    lon = -122.4194155
    radio = 2500
    center = [37.782915476387004, -122.407938144529]
    zomatodict = api.getZomatoCityID("San Francisco")
    rests = api.getStarbucks(zomatodict["id"])
    print(rests)
    rests["distance"] = rests.apply(lambda x: api.addDistance(x["lat"], x["lon"],center), axis = 1)
    rests = rests.sort_values(by=['distance'])
    print(rests)