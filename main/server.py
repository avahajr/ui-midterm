from flask import Flask
from flask import render_template
from flask import Response, request, jsonify

app = Flask(__name__)

current_id = 1
data = [{
    "id": "1",
    "market_name": "Columbia Greenmarket",
    "borough": "Manhattan",
    "image": "https://s3-media0.fl.yelpcdn.com/bphoto/2zligjUgwCXQUlZ5N3lbtw/o.jpg",
    "street_address": "Broadway & 114th street",
    "days": ["Thursday", "Sunday"],
    "year_round": "true",
    "latitude": 40.80714,
    "longitude": -73.96426,
    "vendors_list": ["bread guy", "lavender guy", "farmer1"],
    "summary": "Open year-round on Thursdays and Sundays, this market is located on Broadway along the west side of the Columbia campus from 114th street to 116th street and is one block from St Luke’s Roosevelt Hospital.  It serves a diverse population including university students, faculty and staff, St Luke's Hospital staff, visitors and patients as well as Upper West Side residents. While several of the farmers attend on both Thursday and Sunday, each day has its own distinct character. Thursdays market thrives on the bustle of the work and school day schedule, while Sundays are more laid back and neighbors come out to do serious shopping.  Shoppers will find milk and yogurt, fruit, cider, baked goods, preserved fruits and vegetables, eggs, cheese, smoked meats, pickled vegetables, maple syrup, honey, fish, and focaccia topped with locally sourced fruit, vegetables, herbs and cheeses, a lunch time favorite."
},
    {"id": "2",
     "market_name": "Harvest Home East Harlem Farmers Market",
     "borough": "Manhattan",
     "image": "https://images.happycow.net/venues/1024/15/31/hcmp15312_1147624.jpeg",
     "street_address": "E. 104th St. & 3rd Ave.",
     "days": ["Thursday"],
     "year_round": "false",
     "latitude": 40.7903,
     "longitude": -73.945635,
     "vendors_list": ["bread guy", "lavender guy", "farmer1"],
     "summary": "Harvest Home Farmer’s Market provides low-income communities with access to farm fresh local produce and the education to achieve healthier lifestyles. Harvest Home Farmer's Market is a New York City-based, 501(c)3, non-profit organization dedicated to increasing access to local, farm-fresh produce in low-income neighborhoods. Founded in 1993, our markets create community gathering places that educate the public about health and nutrition, supports regional agriculture and provides job opportunities. Our farmer's markets are open six days a week during the farmer's market season; serving all members of each community."
     },
    {
        "id": "3",
        "market_name": "Seeds in the Middle - Flatbush - Hillel Plaza Farm Stand",
        "borough": "Brooklyn",
        "image": "https://bklyner.com/content/images/bklyner/wp-content/uploads/2020/07/7FD78C1A-F7B9-4878-B01C-76678E710F4F-rotated-e1601416417736.jpeg",
        "street_address": "Flatbush/Nostrand Triangle",
        "days": ["Wednesday"],
        "year_round": "false",
        "latitude": 40.63262,
        "longitude": -73.947439,
        "vendors_list": ["fresh produce guy", "organic snacks seller", "local honey vendor"],
        "summary": "Seeds in the Middle operates a vibrant and community-centric farmers market known as Hillel Plaza Farm Stand, situated in the heart of Brooklyn at Flatbush/Nostrand Triangle. Open every Wednesday, this market offers a delightful assortment of fresh produce, organic snacks, and locally sourced honey. The market is a hub for residents to connect, explore healthy food options, and support local vendors who take pride in providing high-quality, sustainable products."
    },
    {
        "id": "4",
        "market_name": "Morris Heights Farmstand",
        "borough": "Bronx",
        "image": "https://www.brooklynpaper.com/wp-content/uploads/2021/10/IMG-2904-1-1536x1152.jpg",
        "street_address": "University Ave. and W. 179th St.",
        "days": ["Wednesday"],
        "year_round": "false",
        "latitude": 40.854567,
        "longitude": -73.854567,
        "vendors_list": ["farmers cooperative", "vegetable specialists", "local bakers"],
        "summary": "Morris Heights Farmstand, nestled in the Bronx at the intersection of University Ave. and W. 179th St., is a weekly haven for those seeking a diverse array of locally sourced produce and artisanal goods. Every Wednesday, the market comes alive with the energy of a cooperative of farmers, vegetable specialists, and skilled local bakers. Visitors can explore the vibrant offerings, engage with the community, and enjoy the unique flavors that Morris Heights Farmstand brings to this borough."
    },
    {
        "id": "5",
        "market_name": "170 Farm Stand",
        "borough": "Bronx",
        "image": "https://newsettlement.org/food/wp-content/uploads/sites/5/2019/06/20180912_170610.jpg",
        "street_address": "1406 Townsend Ave.",
        "days": ["Wednesday"],
        "year_round": "true",
        "latitude": 40.840138,
        "longitude": -73.916591,
        "vendors_list": ["local farmers", "organic dairy vendor", "artisan bread maker"],
        "summary": "170 Farm Stand, a year-round gem located on 1406 Townsend Ave. in the Bronx, transforms Wednesdays into a celebration of local agriculture and artisanal craftsmanship. Offering a diverse selection of fresh produce from local farmers, organic dairy delights, and the expertise of an artisan bread maker, this market becomes a community focal point. Visitors can savor the seasons, connect with passionate vendors, and experience the vibrant spirit of 170 Farm Stand that echoes the essence of the Bronx."
    },
    {
        "id": "6",
        "market_name": "JBOLC Garden Community Farmers Market",
        "borough": "Bronx",
        "image": "https://jamesbaldwinoutdoorlearningcenter.org/images/jeremy.jpg",
        "street_address": "Sedgwick Ave. & Goulden Ave.",
        "days": ["Saturday"],
        "year_round": "false",
        "latitude": 40.882647,
        "longitude": -73.886562,
        "vendors_list": ["community garden produce", "handcrafted goods", "local artists"],
        "summary": "Nestled at the crossroads of Sedgwick Ave. & Goulden Ave., JBOLC Garden Community Farmers Market is a Saturday gathering that goes beyond providing fresh produce. This market serves as a platform for the community to discover the beauty of community garden produce, explore handcrafted goods, and appreciate the talents of local artists. The vibrancy of JBOLC Garden Community Farmers Market on Saturdays extends beyond transactions, fostering connections, and creating a unique space where residents can experience the creativity and diversity of the Bronx."
    },
    {
        "id": "7",
        "market_name": "Perez Farm Stand",
        "borough": "Queens",
        "image": "https://i.pinimg.com/originals/67/50/e9/6750e9ab2ee4d790e1c908b61c5afc84.jpg",
        "street_address": "134-20 Jamaica Ave., by the Axel Building",
        "days": ["Wednesday"],
        "year_round": "false",
        "latitude": 40.70236,
        "longitude": -73.818531,
        "vendors_list": ["local farmers", "fresh flowers vendor", "artisanal cheese seller"],
        "summary": "Queens comes alive with the colors and flavors of Perez Farm Stand, a Wednesday market located at 134-20 Jamaica Ave. near the Axel Building. Residents and visitors alike can explore a curated selection of fresh produce from local farmers, indulge in the fragrance of fresh flowers, and discover unique artisanal cheeses. Perez Farm Stand transforms midweek shopping into a sensory experience, inviting everyone to connect with the community and savor the diverse offerings that make Queens a culinary destination."
    },
    {
        "id": "8",
        "market_name": "7th Ave Sunset Park Greenmarket",
        "borough": "Brooklyn",
        "image": "https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Ftse3.mm.bing.net%2Fth%3Fid%3DOIP.FfmFZDfm_GF649MXgBWEWgHaFl%26pid%3DApi&f=1&ipt=3235eb34553a5c93a985eb1bbf6be0a70b208aa313206abc3de67d0a5c0bad5a&ipo=images",
        "street_address": "7th Ave. & 44th St.",
        "days": ["Saturday"],
        "year_round": "true",
        "latitude": 40.645841,
        "longitude": -74.002402,
        "vendors_list": ["organic produce farmers", "local honey purveyor", "fresh seafood vendor"],
        "summary": "Embracing the vibrant spirit of Brooklyn, the 7th Ave Sunset Park Greenmarket stands as a beacon of freshness and community on Saturdays. Located at the intersection of 7th Ave. & 44th St., this year-round market showcases the best of local agriculture with organic produce, the sweetness of local honey, and the catch of the day from fresh seafood vendors. Beyond a mere market, it becomes a weekend destination, inviting residents to savor the flavors, support local farmers, and revel in the unique atmosphere that makes Brooklyn's markets truly special."
    },
    {
        "id": "9",
        "market_name": "PS 11 Farm Market",
        "borough": "Manhattan",
        "image": "https://www.amny.com/wp-content/uploads/2013/07/July3CN_p12_PS11Weigh.jpg",
        "street_address": "320 W. 21st St.",
        "days": ["Wednesday"],
        "year_round": "false",
        "latitude": 40.744349,
        "longitude": -74.000253,
        "vendors_list": ["local school garden produce", "homemade jams and preserves", "artisanal chocolates"],
        "summary": "PS 11 Farm Market, nestled at 320 W. 21st St. in the heart of Manhattan, offers a Wednesday escape into a world of unique flavors and artisanal delights. Drawing from a local school garden, this market features a delightful array of fresh produce, homemade jams, and artisanal chocolates. Beyond a marketplace, PS 11 Farm Market becomes a venue for educational exploration and culinary discovery, inviting residents to connect with the community while savoring the distinct offerings of this Manhattan gem."
    },
    {
        "id": "10",
        "market_name": "Astor Place Greenmarket",
        "borough": "Manhattan",
        "image": "https://greenwichvillage.nyc/wp-content/uploads/2022/05/DSC_0837-1200x798.jpeg",
        "street_address": "E. 8th St. & Lafayette",
        "days": ["Tuesday"],
        "year_round": "true",
        "latitude": 40.72982,
        "longitude": -73.991023,
        "vendors_list": ["organic vegetable farmers", "local dairy products", "artisan bread and pastries"],
        "summary": "Astor Place Greenmarket, nestled at the crossroads of E. 8th St. & Lafayette, is a Tuesday haven for Manhattan residents seeking a blend of organic delights and artisanal craftsmanship. Operating year-round, this market brings together a collective of organic vegetable farmers, purveyors of local dairy products, and skilled artisans crafting bread and pastries. Astor Place Greenmarket transforms weekday shopping into a delightful culinary experience, inviting residents to explore, connect, and indulge in the diverse flavors that define this iconic Manhattan market."
    }
]

top3 = data[:3]
def get_results(search_term):
    global data
    return [record for record in data if search_term.lower() in record['market_name'].lower()]

# ROUTES
# Home page
@app.route('/')
def home():
    return render_template('home.html', top3=top3)


@app.route('/search', methods=['POST', 'GET'])
def search():
    search_term = request.json['search_term']
    results = get_results(search_term)
    msg = f"No results found for '{search_term}'" if len(results) == 0 else f"Showing results for '{search_term}'"
    return render_template('search.html', results=results, msg=msg)




# AJAX FUNCTIONS

# ajax for farmer.js
# @app.route('/add_name', methods=['GET', 'POST'])
# def add_name():
#     global data
#     global current_id
#
#     json_data = request.get_json()
#     name = json_data["name"]
#
#     # add new entry to array with
#     # a new id and the name the user sent in JSON
#     current_id += 1
#     new_id = current_id
#     new_name_entry = {
#         "name": name,
#         "id":  current_id
#     }
#     data.append(new_name_entry)
#
#     #send back the WHOLE array of data, so the client can redisplay it
#     return jsonify(data = data)



if __name__ == '__main__':
    app.run(debug=True, port=6969)
