from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, redirect
import json
from amenities_manager.forms import DocumentForm
from amenities_manager.models import Document, FileManagerDocument
import os
import geojson
import os.path, time
import io
from matplotlib import pyplot as plt
import shapely
from shapely.geometry.polygon import LinearRing, Polygon
from shapely.geometry.multipolygon import MultiPolygon
from django.shortcuts import render_to_response
from django.contrib import messages
from django.utils.safestring import mark_safe


def index(request):
    context = {}
    return render(request, 'amenities_manager/File-Manager.html', context)


#def manage(request):
#    with open('media/amenities/amenitiesgeojson.json', encoding="utf-8") as f:
#        json_data = json.load(f)
#    context = {
#        'amenities': json.dumps(json_data)
#    }
#    return render(request, 'Amenities-Manager.html', context)

def manage(request, filename):
    print(filename)
    with open('media/amenities/' + filename, encoding="utf-8") as f:
            json_data = json.load(f)
            context = {
                'amenities': mark_safe(json_data),
                'filename': filename
            }

    return render(request, 'Amenities-Manager.html', context)


#def manageLoad(request):
   # return render(request, 'Amenities-Manager.html', context)


def manageSave(request, filename):
    if request.is_ajax() and request.POST:
        data = request.POST.get('amenities')
        print("DATA: " + str(data))
        dump = geojson.loads(data)
    # f = open("media/amenities/amenitiesedited.json", 'w', encoding="utf-8")
    # f.write("[\n")
    # ctr = 0
    # for item in data:
    #     if ctr != 0:
    #         f.write(",\n")
    #     f.write(data[ctr])
    #     ctr = ctr + 1
    # f.write("\n]")
    # f.close()

        geom_in_geojson = geojson.loads(data)
        with open("media/amenities/" + filename, 'w', encoding="utf-8") as outfile:
            geojson.dump(geom_in_geojson, outfile, indent=4, sort_keys=True)
    #return tmp_file[1]
        return HttpResponse("got the json")

    return render(request, 'Amenities-Manager.html')


def choose(request):
    amenity_directory = "media/amenities"
    file_manager_page_title = "Amenities"
    if not os.path.exists(amenity_directory):
        os.makedirs(amenity_directory)

    amenity_documents = []
    amenity_filelist = os.listdir(amenity_directory)
    for file in amenity_filelist:
        amenity_file = FileManagerDocument()
        amenity_file.doc_name = file
        print("PATH: " + amenity_directory + "/" + file)
        formatted_time = time.strftime('%B %d, %Y', time.gmtime(os.path.getmtime(amenity_directory + "/" + file)))
        amenity_file.date_modified = formatted_time
        amenity_documents.append(amenity_file)

    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        print("BEFORE WENT IN VALID")
        if form.is_valid():
            print("WENT IN VALID")
            newfile = Document()
            newfile.document = form.cleaned_data["docfile"]
            original_name, extension = os.path.splitext(newfile.document.name)
            newfile.document.name = "amenities/" + original_name + extension
            newfile.doc_name = original_name
            newfile.save()
            cleanAmenities(original_name, extension)
            print("done cleaning amenities")
            #return redirect('choose')
    else:
        form = DocumentForm()

    return render(request, 'File-Manager.html', {
        'form': form,
        'filemanager_filenames': amenity_documents,
        'file_manager_page_title': file_manager_page_title
    })


def cleanAmenities(source, srcExtension):
    print("in cleaning amenities + " + source + srcExtension)
    type = "amenity"
    if srcExtension == ".json":
        f = io.open("media/amenities/" + source + "_cleaned.geojson", 'w', encoding="utf-8")
        f.write("{\"type\": \"FeatureCollection\",")
        f.write("\"generator\": \"overpass-turbo\",")
        f.write("\"copyright\": \"The data included in this document is from www.openstreetmap.org. The data is made available under ODbL.\",")
        f.write("\"timestamp\": \"2017-03-19T12:47:02Z\",")
        f.write("\"features\":")
        f.write("[\n")
        ctr = 0
        index = -1
        with io.open("media/amenities/" + source + ".json", encoding="utf-8") as z:
            m = json.load(z)
            for data in m:
                if ctr != 0:
                    f.write(",\n")
                else:
                    ctr = ctr + 1
                index = index + 1
                if (data['amenity_type'] == "bar" or
                            data['amenity_type'] == "restaurant" or
                            data['amenity_type'] == "bbq" or
                            data['amenity_type'] == "cafe" or
                            data['amenity_type'] == "pub" or
                            data['amenity_type'] == "restaurant" or
                            data['amenity_type'] == "fast_food" or
                            data['amenity_type'] == "food_court" or
                            data['amenity_type'] == "ice_cream" or
                            data['amenity_type'] == "biergarten" or
                            data['amenity_type'] == "drinking_water" or
                            data['amenity_type'] == "water_point" or
                            data['amenity_type'] == "vending_machine" or
                            data['amenity_type'] == "baking_oven"):
                    data['amenity_type'] = "sustenance"
                elif (data['amenity_type'] == "college" or
                              data['amenity_type'] == "kindergarten" or
                              data['amenity_type'] == "library" or
                              data['amenity_type'] == "public_bookcase" or
                              data['amenity_type'] == "school" or
                              data['amenity_type'] == "music_school" or
                              data['amenity_type'] == "driving_school" or
                              data['amenity_type'] == "language_school" or
                              data['amenity_type'] == "university"):
                    data['amenity_type'] = "education"
                elif (data['amenity_type'] == "clinic" or
                              data['amenity_type'] == "dentist" or
                              data['amenity_type'] == "doctors" or
                              data['amenity_type'] == "hospital" or
                              data['amenity_type'] == "nursing_home" or
                              data['amenity_type'] == "pharmacy" or
                              data['amenity_type'] == "veterenary" or
                              data['amenity_type'] == "blood_donation"):
                    data['amenity_type'] = "healthcare"
                elif (data['amenity_type'] == "bicycle_parking" or
                              data['amenity_type'] == "bicycle_repair_station" or
                              data['amenity_type'] == "bicycle_rental" or
                              data['amenity_type'] == "boat_sharing" or
                              data['amenity_type'] == "bus_station" or
                              data['amenity_type'] == "car_rental" or
                              data['amenity_type'] == "car_sharing" or
                              data['amenity_type'] == "car_wash" or
                              data['amenity_type'] == "motorcycle_parking" or
                              data['amenity_type'] == "parking" or
                              data['amenity_type'] == "parking_entrance" or
                              data['amenity_type'] == "parking_space" or
                              data['amenity_type'] == "charging_station" or
                              data['amenity_type'] == "ferry_terminal" or
                              data['amenity_type'] == "fuel" or
                              data['amenity_type'] == "taxi"):
                    data['amenity_type'] = "transport"
                elif (data['amenity_type'] == "atm" or
                              data['amenity_type'] == "bank" or
                              data['amenity_type'] == "bureau_de_change"):
                    data['amenity_type'] = "finance"
                elif (data['amenity_type'] == "internet_cafe" or
                              data['amenity_type'] == "kneipp_water_cure" or
                              data['amenity_type'] == "marketplace" or
                              data['amenity_type'] == "photo_booth" or
                              data['amenity_type'] == "dojo" or
                              data['amenity_type'] == "animal_shelter" or
                              data['amenity_type'] == "gym" or
                              data['amenity_type'] == "animal_boarding" or
                              data['amenity_type'] == "ranger_station" or
                              data['amenity_type'] == "hunting_stand" or
                              data['amenity_type'] == "sauna"):
                    data['amenity_type'] = "commerce"
                elif (data['amenity_type'] == "social_facility" or
                              data['amenity_type'] == "arts_centre" or
                              data['amenity_type'] == "casino" or
                              data['amenity_type'] == "gambling" or
                              data['amenity_type'] == "theatre" or
                              data['amenity_type'] == "planetarium" or
                              data['amenity_type'] == "cinema" or
                              data['amenity_type'] == "dive_centre" or
                              data['amenity_type'] == "game_feeding" or
                              data['amenity_type'] == "stripclub" or
                              data['amenity_type'] == "nightclub" or
                              data['amenity_type'] == "swingerclub" or
                              data['amenity_type'] == "brothel" or
                              data['amenity_type'] == "studio"):
                    data['amenity_type'] = "entertainment"
                elif (data['amenity_type'] == "baby_hatch" or
                              data['amenity_type'] == "community_centre" or
                              data['amenity_type'] == "fountain" or
                              data['amenity_type'] == "social_centre" or
                              data['amenity_type'] == "firepit" or
                              data['amenity_type'] == "bench" or
                              data['amenity_type'] == "clock" or
                              data['amenity_type'] == "courthouse" or
                              data['amenity_type'] == "crematorium" or
                              data['amenity_type'] == "crypt" or
                              data['amenity_type'] == "townhall" or
                              data['amenity_type'] == "grave_yard" or
                              data['amenity_type'] == "telephone" or
                              data['amenity_type'] == "toilets" or
                              data['amenity_type'] == "shower" or
                              data['amenity_type'] == "place_of_worship" or
                              data['amenity_type'] == "police" or
                              data['amenity_type'] == "table" or
                              data['amenity_type'] == "shelter" or
                              data['amenity_type'] == "embassy" or
                              data['amenity_type'] == "fire_station" or
                              data['amenity_type'] == "rescue_station" or
                              data['amenity_type'] == "public_building" or
                              data['amenity_type'] == "post_box" or
                              data['amenity_type'] == "post_office" or
                              data['amenity_type'] == "prison" or
                              data['amenity_type'] == "recycling" or
                              data['amenity_type'] == "waste_basket" or
                              data['amenity_type'] == "waste_disposal" or
                              data['amenity_type'] == "waste_transfer_station" or
                              data['amenity_type'] == "grit_bin" or
                              data['amenity_type'] == "watering_place"):
                    data['amenity_type'] = "other"
                f.write("{\"type\": \"Feature\", \"properties\": {")
                f.write("\"id\": \"" + str(index) + "\", ")
                f.write("\"name\": \"" + str.replace(data['name'], '\\', '\\\\')+ "\", ")
                f.write("\"latitude\": \"" + str(data['latitude']) + "\", ")
                f.write("\"longitude\": \"" + str(data['long']) + "\", ")
                f.write("\"capacity\": \"200\", ")
                f.write("\"amenity_type\": \"" + data['amenity_type'] + "\"},")
                f.write("\"geometry\": {\"type\": \"Point\",")
                f.write("\"coordinates\": [" + str(data['long']) + ", " + str(data['latitude']) + "]}")
                f.write("}")
        f.write("\n]")
        f.write("}")
        f.close()
        z.close()
    elif srcExtension == ".geojson":
        f = io.open("media/amenities/" + source + "_cleaned.geojson", 'w', encoding="utf-8")
        f.write("{\"type\": \"FeatureCollection\",")
        f.write("\"generator\": \"overpass-turbo\",")
        f.write("\"copyright\": \"The data included in this document is from www.openstreetmap.org. The data is made available under ODbL.\",")
        f.write("\"timestamp\": \"2017-03-19T12:47:02Z\",")
        f.write("\"features\":")
        f.write("[\n")
        ctr = 0
        index = -1
        with io.open("media/amenities/" + source + ".geojson", encoding="utf-8") as z:
            m = json.load(z)
            for data in m['features']:
                if ctr != 0:
                    f.write(",\n")
                else:
                    ctr = ctr + 1
                index = index + 1

                if ('shop' in data['properties'] and 'amenity_type' not in data['properties']):
                    data['properties']['amenity_type'] = "commerce"
                    type = "shop"
                    print("is a shop " + data['properties']['amenity_type'])
                elif 'office' in data['properties']:
                    data['properties']['amenity_type'] = "other"
                    type = "office"
                    print("is office")
                elif('shop' not in data['properties'] and 'amenity_type' not in data['properties']):
                    data['properties']['amenity_type'] = "commerce"
                    type = "shop"
                    print("is not both shop " + data['properties']['amenity_type'])
                if (data['properties']['amenity_type'] == "bar" or
                            data['properties']['amenity_type'] == "restaurant" or
                            data['properties']['amenity_type'] == "bbq" or
                            data['properties']['amenity_type'] == "cafe" or
                            data['properties']['amenity_type'] == "pub" or
                            data['properties']['amenity_type'] == "restaurant" or
                            data['properties']['amenity_type'] == "fast_food" or
                            data['properties']['amenity_type'] == "food_court" or
                            data['properties']['amenity_type'] == "ice_cream" or
                            data['properties']['amenity_type'] == "biergarten" or
                            data['properties']['amenity_type'] == "drinking_water" or
                            data['properties']['amenity_type'] == "water_point" or
                            data['properties']['amenity_type'] == "vending_machine" or
                            data['properties']['amenity_type'] == "baking_oven"):
                    data['properties']['amenity_type'] = "sustenance"
                elif (data['properties']['amenity_type'] == "college" or
                              data['properties']['amenity_type'] == "kindergarten" or
                              data['properties']['amenity_type'] == "library" or
                              data['properties']['amenity_type'] == "public_bookcase" or
                              data['properties']['amenity_type'] == "school" or
                              data['properties']['amenity_type'] == "music_school" or
                              data['properties']['amenity_type'] == "driving_school" or
                              data['properties']['amenity_type'] == "language_school" or
                              data['properties']['amenity_type'] == "university"):
                    data['properties']['amenity_type'] = "education"
                elif (data['properties']['amenity_type'] == "clinic" or
                              data['properties']['amenity_type'] == "dentist" or
                              data['properties']['amenity_type'] == "doctors" or
                              data['properties']['amenity_type'] == "hospital" or
                              data['properties']['amenity_type'] == "nursing_home" or
                              data['properties']['amenity_type'] == "pharmacy" or
                              data['properties']['amenity_type'] == "veterenary" or
                              data['properties']['amenity_type'] == "blood_donation"):
                    data['properties']['amenity_type'] = "healthcare"
                elif (data['properties']['amenity_type'] == "bicycle_parking" or
                              data['properties']['amenity_type'] == "bicycle_repair_station" or
                              data['properties']['amenity_type'] == "bicycle_rental" or
                              data['properties']['amenity_type'] == "boat_sharing" or
                              data['properties']['amenity_type'] == "bus_station" or
                              data['properties']['amenity_type'] == "car_rental" or
                              data['properties']['amenity_type'] == "car_sharing" or
                              data['properties']['amenity_type'] == "car_wash" or
                              data['properties']['amenity_type'] == "motorcycle_parking" or
                              data['properties']['amenity_type'] == "parking" or
                              data['properties']['amenity_type'] == "parking_entrance" or
                              data['properties']['amenity_type'] == "parking_space" or
                              data['properties']['amenity_type'] == "charging_station" or
                              data['properties']['amenity_type'] == "ferry_terminal" or
                              data['properties']['amenity_type'] == "fuel" or
                              data['properties']['amenity_type'] == "taxi"):
                    data['properties']['amenity_type'] = "transport"
                elif (data['properties']['amenity_type'] == "atm" or
                              data['properties']['amenity_type'] == "bank" or
                              data['properties']['amenity_type'] == "bureau_de_change"):
                    data['properties']['amenity_type'] = "finance"
                elif (data['properties']['amenity_type'] == "internet_cafe" or
                              data['properties']['amenity_type'] == "kneipp_water_cure" or
                              data['properties']['amenity_type'] == "marketplace" or
                              data['properties']['amenity_type'] == "photo_booth" or
                              data['properties']['amenity_type'] == "dojo" or
                              data['properties']['amenity_type'] == "animal_shelter" or
                              data['properties']['amenity_type'] == "gym" or
                              data['properties']['amenity_type'] == "animal_boarding" or
                              data['properties']['amenity_type'] == "ranger_station" or
                              data['properties']['amenity_type'] == "hunting_stand" or
                              data['properties']['amenity_type'] == "sauna"):
                    data['properties']['amenity_type'] = "commerce"
                elif (data['properties']['amenity_type'] == "social_facility" or
                              data['properties']['amenity_type'] == "arts_centre" or
                              data['properties']['amenity_type'] == "casino" or
                              data['properties']['amenity_type'] == "gambling" or
                              data['properties']['amenity_type'] == "theatre" or
                              data['properties']['amenity_type'] == "planetarium" or
                              data['properties']['amenity_type'] == "cinema" or
                              data['properties']['amenity_type'] == "dive_centre" or
                              data['properties']['amenity_type'] == "game_feeding" or
                              data['properties']['amenity_type'] == "stripclub" or
                              data['properties']['amenity_type'] == "nightclub" or
                              data['properties']['amenity_type'] == "swingerclub" or
                              data['properties']['amenity_type'] == "brothel" or
                              data['properties']['amenity_type'] == "studio"):
                    data['properties']['amenity_type'] = "entertainment"
                elif (data['properties']['amenity_type'] == "baby_hatch" or
                              data['properties']['amenity_type'] == "community_centre" or
                              data['properties']['amenity_type'] == "fountain" or
                              data['properties']['amenity_type'] == "social_centre" or
                              data['properties']['amenity_type'] == "firepit" or
                              data['properties']['amenity_type'] == "bench" or
                              data['properties']['amenity_type'] == "clock" or
                              data['properties']['amenity_type'] == "courthouse" or
                              data['properties']['amenity_type'] == "crematorium" or
                              data['properties']['amenity_type'] == "crypt" or
                              data['properties']['amenity_type'] == "townhall" or
                              data['properties']['amenity_type'] == "grave_yard" or
                              data['properties']['amenity_type'] == "telephone" or
                              data['properties']['amenity_type'] == "toilets" or
                              data['properties']['amenity_type'] == "shower" or
                              data['properties']['amenity_type'] == "place_of_worship" or
                              data['properties']['amenity_type'] == "police" or
                              data['properties']['amenity_type'] == "table" or
                              data['properties']['amenity_type'] == "shelter" or
                              data['properties']['amenity_type'] == "embassy" or
                              data['properties']['amenity_type'] == "fire_station" or
                              data['properties']['amenity_type'] == "rescue_station" or
                              data['properties']['amenity_type'] == "public_building" or
                              data['properties']['amenity_type'] == "post_box" or
                              data['properties']['amenity_type'] == "post_office" or
                              data['properties']['amenity_type'] == "prison" or
                              data['properties']['amenity_type'] == "recycling" or
                              data['properties']['amenity_type'] == "waste_basket" or
                              data['properties']['amenity_type'] == "waste_disposal" or
                              data['properties']['amenity_type'] == "waste_transfer_station" or
                              data['properties']['amenity_type'] == "grit_bin" or
                              data['properties']['amenity_type'] == "watering_place"):
                    data['properties']['amenity_type'] = "other"
                f.write("{\"type\": \"Feature\", \"properties\": {")
                f.write("\"id\": \"" + str(index) + "\", ")
                if "name" not in data['properties']:
                    data['properties']['name'] = "no name available"
                else:
                    f.write("\"name\": \"" + str.replace(data['properties']['name'], '\\', '\\\\')+ "\", ")
                point = shapely.geometry.geo.shape(data['geometry'])
                if (type == "shop" or type == "office"):
                    f.write("\"latitude\": \"" + str(point.centroid.y) + "\", ")
                else:
                    f.write("\"latitude\": \"" + str(point.y) + "\", ")
                if (type == "shop" or type == "office"):
                    f.write("\"longitude\": \"" + str(point.centroid.x) + "\", ")
                else:
                    f.write("\"longitude\": \"" + str(point.x) + "\", ")
                f.write("\"capacity\": \"200\", ")
                f.write("\"amenity_type\": \"" + data['properties']['amenity_type'] + "\"},")
                f.write("\"geometry\": {\"type\": \"Point\",")
                if (type == "shop" or type == "office"):
                    f.write("\"coordinates\": [" + str(point.centroid.x) + ", " + str(point.centroid.y) + "]}")
                else:
                    f.write("\"coordinates\": [" + str(point.x) + ", " + str(point.y) + "]}")
                f.write("}")
        f.write("\n]")
        f.write("}")
        f.close()
        z.close()
