import api



if __name__=='__main__':
    test = input("Localizacion: ")
    print(test)
    print(api.getGeoloc(test))
    zomatodict = api.getZomatoCityID(test)
    rests = api.getVeganRestaurants(zomatodict["id"])
    starbucks = api.getStarbucks(zomatodict["id"])
    print(zomatodict)
    print(rests)
    print(starbucks)