from pymongo import MongoClient
import pandas as pd
import json

def geopoint(x): 
    latitude = 20
    longitude = 20
    for comp in x:   
        latitude = comp["latitude"]
        longitude = comp["longitude"]
        if latitude is None:
            return {"type": "Point", "coordinates": [20,20]}
        return {"type": "Point", "coordinates": [longitude,latitude]}
    return {"type": "Point", "coordinates": [longitude,latitude]}

def geonear(geopoint, maxdistance=1000):
    return db.companiesfil.find({
        "geo":{
            "$near":{
                "$geometry":geopoint,
                "$maxDistance":maxdistance
            }}})
    
# conexión con la base de datos de mongo
client = MongoClient("mongodb://localhost:27017/")
db = client.companies 

# filtrado y creación de dataframe
companies_filtered = db.companies.find({
    "acquisition.price_amount":{"$gt":10000000},
    "category_code": {"$in":['software', 'games_video', 'advertising', 'social', 'music', 'travel', 'sports', 'design', 'other']
                     }})

companies_filtered = pd.DataFrame(companies_filtered)

# Me quedo con las columnas que quiero
companies_filt = companies_filtered[["acquisition","acquisitions","category_code","created_at","crunchbase_url","description",
"founded_year","homepage_url","name","number_of_employees","offices","overview","products","total_money_raised"]]

# Le aplico la función de geopoint para obtener las coordenadas de la primera oficina de cada compañia
companies_filt["geo"] = companies_filt["offices"].apply(geopoint)

# Lo exporto a json
companies_filt.to_json("./geocompanies.json",orient='records')

# Esta es otra opción que lo pasa mete directamente sin tener que hacer el mongoimport
#records = json.loads(companies_filt.T.to_json()).values()
#db.companiesfilt.insert_many(records)

# Vuelvo a importar la colección y lo paso a un DF
companiesfil = db.companiesfil.find()
dfcompaniesfil = pd.DataFrame(companiesfil)

# Algunas coordenadas de interés
fifth_avenue = {'type': 'Point', 'coordinates': [-73.9678246, 40.7744089]}
mountain_view = {'type': 'Point', 'coordinates': [-122.086419, 37.387120]}
microsoft = {'type': 'Point', 'coordinates': [-122.071367, 37.412692]}

# Creo un DF con los resultados que esten cerca
df_test = pd.DataFrame(geonear(microsoft,3000))