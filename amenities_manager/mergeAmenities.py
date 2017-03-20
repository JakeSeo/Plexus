from matplotlib import pyplot as plt
import shapely
from shapely.geometry.polygon import LinearRing, Polygon
from shapely.geometry.multipolygon import MultiPolygon
import json
import geojson
import os
import io

f = io.open("../media/amenities/AmenitiesConcat.json", "w", encoding="utf-8")
f.write("[\n")
ctr = 0
index = -1
with io.open("../media/amenities/Amenities.json", encoding="utf-8") as amenitiesFile:
    amenities = json.load(amenitiesFile)
    for data in amenities:
        if ctr != 0:
            f.write(",\n")
        else:
            ctr = ctr + 1
        index = index + 1
        f.write("{\"type\": \"Feature\", \"properties\": {")
        f.write("\"id\": \"" + str(index) + "\", ")
        f.write("\"name\": \"" + data['properties']['name'] + "\", ")
        f.write("\"latitude\": \"" + str(data['properties']['latitude']) + "\", ")
        f.write("\"longitude\": \"" + str(data['properties']['longitude']) + "\", ")
        f.write("\"capacity\": \"200\", ")
        f.write("\"amenity_type\": \"" + data['properties']['amenity_type'] + "\"},")
        f.write("\"geometry\": {\"type\": \"Point\",")
        f.write("\"coordinates\": [" + str(data['properties']['longitude']) + ", " + str(data['properties']['latitude']) + "]}")
        f.write("}")
amenitiesFile.close()


with io.open("../media/amenities/Shops.geojson", encoding="utf-8") as shopsFile:
    amenities = json.load(shopsFile)
    for data in amenities['features']:
        if ctr != 0:
            f.write(",\n")
        else:
            ctr = ctr + 1
        index = index + 1
        f.write("{\"type\": \"Feature\", \"properties\": {")
        f.write("\"id\": \"" + str(index) + "\", ")
        if "name" not in data['properties']:
            data['properties']['name'] = "no name available"
        f.write("\"name\": \"" + data['properties']['name'] + "\", ")
        polygon = shapely.geometry.geo.shape(data['geometry'])
        f.write("\"latitude\": \"" + str(polygon.centroid.x) + "\", ")
        f.write("\"longitude\": \"" + str(polygon.centroid.y) + "\", ")
        f.write("\"capacity\": \"100\", ")
        if "shop" not in data['properties']:
            data['properties']['shop'] = "commerce"
        if (data['properties']['shop'] == "alcohol" or
        data['properties']['shop'] == "bakery" or
        data['properties']['shop'] == "beverages" or
        data['properties']['shop'] == "brewing_supplies" or
        data['properties']['shop'] == "butcher" or
        data['properties']['shop'] == "cheese" or
        data['properties']['shop'] == "chocolate" or
        data['properties']['shop'] == "coffee" or
        data['properties']['shop'] == "confectionery" or
        data['properties']['shop'] == "convenience" or
        data['properties']['shop'] == "deli" or
        data['properties']['shop'] == "dairy" or
        data['properties']['shop'] == "farm" or
        data['properties']['shop'] == "greengrocer" or
        data['properties']['shop'] == "ice_cream" or
        data['properties']['shop'] == "organic" or
        data['properties']['shop'] == "pasta" or
        data['properties']['shop'] == "pastry" or
        data['properties']['shop'] == "seafood" or
        data['properties']['shop'] == "spices" or
        data['properties']['shop'] == "tea" or
        data['properties']['shop'] == "wine"):
            data['properties']['shop'] = "sustenance"
        elif (data['properties']['shop'] == "department_store" or
        data['properties']['shop'] == "general" or
        data['properties']['shop'] == "kiosk" or
        data['properties']['shop'] == "mall" or
        data['properties']['shop'] == "supermarket" or
        data['properties']['shop'] == "baby_goods" or
        data['properties']['shop'] == "bag" or
        data['properties']['shop'] == "boutique" or
        data['properties']['shop'] == "clothes" or
        data['properties']['shop'] == "fabric" or
        data['properties']['shop'] == "fashion" or
        data['properties']['shop'] == "jewelry" or
        data['properties']['shop'] == "leather" or
        data['properties']['shop'] == "shoes" or
        data['properties']['shop'] == "tailor" or
        data['properties']['shop'] == "watches" or
        data['properties']['shop'] == "charity" or
        data['properties']['shop'] == "second_hand" or
        data['properties']['shop'] == "variety_store" or
        data['properties']['shop'] == "beauty" or
        data['properties']['shop'] == "chemist" or
        data['properties']['shop'] == "cosmetics" or
        data['properties']['shop'] == "erotic" or
        data['properties']['shop'] == "hairdresser" or
        data['properties']['shop'] == "hairdresser_supply" or
        data['properties']['shop'] == "perfumery" or
        data['properties']['shop'] == "tattoo" or
        data['properties']['shop'] == "agrarian" or
        data['properties']['shop'] == "bathroom_furnishing" or
        data['properties']['shop'] == "doityourself" or
        data['properties']['shop'] == "electrical" or
        data['properties']['shop'] == "energy" or
        data['properties']['shop'] == "fireplace" or
        data['properties']['shop'] == "florist" or
        data['properties']['shop'] == "garden_centre" or
        data['properties']['shop'] == "garden_furniture" or
        data['properties']['shop'] == "gas" or
        data['properties']['shop'] == "glaziery" or
        data['properties']['shop'] == "hardware" or
        data['properties']['shop'] == "houseware" or
        data['properties']['shop'] == "locksmith" or
        data['properties']['shop'] == "paint" or
        data['properties']['shop'] == "security" or
        data['properties']['shop'] == "trade" or
        data['properties']['shop'] == "antiques" or
        data['properties']['shop'] == "bed" or
        data['properties']['shop'] == "candles" or
        data['properties']['shop'] == "carpet" or
        data['properties']['shop'] == "curtain" or
        data['properties']['shop'] == "furniture" or
        data['properties']['shop'] == "interior_decoration" or
        data['properties']['shop'] == "kitchen" or
        data['properties']['shop'] == "lamps" or
        data['properties']['shop'] == "tiles" or
        data['properties']['shop'] == "window_blind" or
        data['properties']['shop'] == "computer" or
        data['properties']['shop'] == "electronics" or
        data['properties']['shop'] == "hifi" or
        data['properties']['shop'] == "mobile_phone" or
        data['properties']['shop'] == "radiotechnics" or
        data['properties']['shop'] == "vacuum_cleaner" or
        data['properties']['shop'] == "outdoor" or
        data['properties']['shop'] == "scuba_diving" or
        data['properties']['shop'] == "sports" or
        data['properties']['shop'] == "swimming_pool" or
        data['properties']['shop'] == "art" or
        data['properties']['shop'] == "collector" or
        data['properties']['shop'] == "craft" or
        data['properties']['shop'] == "frame" or
        data['properties']['shop'] == "games" or
        data['properties']['shop'] == "model" or
        data['properties']['shop'] == "music" or
        data['properties']['shop'] == "musical_instrument" or
        data['properties']['shop'] == "photo" or
        data['properties']['shop'] == "camera" or
        data['properties']['shop'] == "trophy" or
        data['properties']['shop'] == "video" or
        data['properties']['shop'] == "video_games" or
        data['properties']['shop'] == "anime" or
        data['properties']['shop'] == "books" or
        data['properties']['shop'] == "gift" or
        data['properties']['shop'] == "lottery" or
        data['properties']['shop'] == "newsagent" or
        data['properties']['shop'] == "stationery" or
        data['properties']['shop'] == "ticket" or
        data['properties']['shop'] == "bookmaker" or
        data['properties']['shop'] == "copyshop" or
        data['properties']['shop'] == "dry_cleaning" or
        data['properties']['shop'] == "e_cigarette" or
        data['properties']['shop'] == "funeral_directors" or
        data['properties']['shop'] == "laundry" or
        data['properties']['shop'] == "pet" or
        data['properties']['shop'] == "pyrotechnics" or
        data['properties']['shop'] == "religion" or
        data['properties']['shop'] == "tobacco" or
        data['properties']['shop'] == "toys" or
        data['properties']['shop'] == "travel_agency" or
        data['properties']['shop'] == "vacant" or
        data['properties']['shop'] == "weapons" or
        data['properties']['shop'] == "user defined" or
        data['properties']['shop'] == "bicycle" or
        data['properties']['shop'] == "car" or
        data['properties']['shop'] == "car_repair" or
        data['properties']['shop'] == "car_parts" or
        data['properties']['shop'] == "fuel" or
        data['properties']['shop'] == "fishing" or
        data['properties']['shop'] == "free_flying" or
        data['properties']['shop'] == "hunting" or
        data['properties']['shop'] == "motorcycle" or
        data['properties']['shop'] == "tyres"):
            data['properties']['shop'] = "commerce"
        elif(data['properties']['shop'] == "money_lender" or
        data['properties']['shop'] == "pawnbroker"):
            data['properties']['shop'] = "finance"
        elif (data['properties']['shop'] == "drugstore" or
        data['properties']['shop'] == "hearing_aids" or
        data['properties']['shop'] == "herbalist" or
        data['properties']['shop'] == "massage" or
        data['properties']['shop'] == "medical_supply" or
        data['properties']['shop'] == "nutrition_supplements" or
        data['properties']['shop'] == "optician"):
            data['properties']['shop'] = "healthcare"
        else: data['properties']['shop'] = "commerce"
        f.write("\"amenity_type\": \"" + data['properties']['shop'] + "\"},")
        f.write("\"geometry\": {\"type\": \"Point\",")
        f.write("\"coordinates\": [" + str(polygon.centroid.y) + ", " + str(polygon.centroid.x) + "]}")
        f.write("}")
shopsFile.close()


with io.open("../media/amenities/Offices.geojson", encoding="utf-8") as officesFile:
    amenities = json.load(officesFile)
    for data in amenities['features']:
        if ctr != 0:
            f.write(",\n")
        else:
            ctr = ctr + 1
        index = index + 1
        f.write("{\"type\": \"Feature\", \"properties\": {")
        f.write("\"id\": \"" + str(index) + "\", ")
        if "name" not in data['properties']:
            data['properties']['name'] = "no name available"
        f.write("\"name\": \"" + data['properties']['name'] + "\", ")
        polygon = shapely.geometry.geo.shape(data['geometry'])
        f.write("\"latitude\": \"" + str(polygon.centroid.x) + "\", ")
        f.write("\"longitude\": \"" + str(polygon.centroid.y) + "\", ")
        f.write("\"capacity\": \"100\", ")
        f.write("\"amenity_type\": \"other\"},")
        f.write("\"geometry\": {\"type\": \"Point\",")
        f.write("\"coordinates\": [" + str(polygon.centroid.y) + ", " + str(polygon.centroid.x) + "]}")
        f.write("}")
officesFile.close()
f.write("\n]")
f.close()