# Enunciado geo_office

You recently created a new company in the `GAMING industry`. The company will have the following scheme:
- 20 Designers
- 5 UI/UX Engineers
- 10 Frontend Developers
- 15 Data Engineers
- 5 Backend Developers
- 20 Account Managers
- 1 Maintenance guy that loves basketball
- 10 Executives
- 1 CEO/President

As a data engineer you have asked all the employees to show their preferences on where to place the new office.
Your goal is to place the **new company offices** in the best place for the company to grow.
You have to found a place that more or less covers all the following requirements.
Note that **it's impossible to cover all requirements**, so you have to prioritize at your glance.
- Designers like to go to design talks and share knowledge. There must be some nearby companies that also do design.
- 30% of the company have at least 1 child.
- Developers like to be near successful tech startups that have raised at least 1 Million dollars.
- Executives like Starbucks A LOT. Ensure there's a starbucks not to far.
- Account managers need to travel a lot
- All people in the company have between 25 and 40 years, give them some place to go to party.
- Nobody in the company likes to have companies with more than 10 years in a radius of 2 KM.
- The CEO is Vegan


# Process

I decided to focus this project differently. I give the company the possibility to choose the best place on a city where to place the new office. So they will need to search for a city and based on the database and their preferences, the system will choose the best place.

First of all I filtered the database with the companies that I wanted. This was my query: `{
    "total_money_raised":{"$regex":'M'},
    "category_code": {"$in":['software', 'games_video', 'advertising', 'social', 'music', 'travel', 'sports', 'design', 'other']
                     }}` 
 Having a total of 1300 companies. After that, I applied a function to make a geopoint and then create an index in MongoDB to be able to use the "$near" function. 

I used the APIs of Google and Zomato. The first one for all the maps, addresses and directions, and the second one to take the location of the best vegetarian restaurants and Starbucks.

I used an airport csv dataset to find out the nearests airports to the location. 

The web was made with bottle and it uses Scrollify.

## Help
- Geospatial range Queries in MongoDB with `pymongo`
- GeoJSON Point `{ type: "Point", coordinates: [ 40, 5 ] }`
- Create sphere2d index in python: `db.collection.createIndex( { <location field> : "2dsphere" } )`
- Query `$near` operator: https://docs.mongodb.com/manual/reference/operator/query/near/#op._S_near
## How to deliver the project
- You must justify your decision with tableau slides. Provide us the public tableau link inside a README.md
  file at dir `module-2/project-mongodb-geospartial-queries`.
- Provide `lat` and `long` for the new offices.
## Links & Resources
- https://docs.mongodb.com/manual/geospatial-queries/
- https://developers.google.com/maps/documentation/geocoding/intro
- https://data.crunchbase.com/docs
- https://developers.google.com/places/web-service/search
- https://www.youtube.com/watch?v=PtV-ZnwCjT0

