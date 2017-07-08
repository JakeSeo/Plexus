from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, redirect
import json
from landuse_manager.forms import DocumentForm
from landuse_manager.models import Document, FileManagerDocument
import os
import os.path, time
from matplotlib import pyplot as plt
import shapely
from shapely.geometry import shape
from shapely.geometry.polygon import LinearRing, Polygon
from shapely.geometry.multipolygon import MultiPolygon
import geojson
import io
from django.utils.safestring import mark_safe


def index(request):
    context = {}
    return render(request, 'landuse_manager/index.html', context)


def manage(request, filename):
    with open('media/landuses/' + filename, encoding="utf-8") as f:
        json_data = json.load(f)
    context = {
        'json_data': mark_safe(json_data),
        'filename': filename
    }
    return render(request, 'landuse_manager/LandUse-Manager.html', context)

def manageSave(request, filename):
    if request.is_ajax() and request.POST:
        data = request.POST.get('landuse')
        print("DATA: " + str(data))

        geom_in_geojson = geojson.loads(data)
        with open("media/landuses/" + filename, 'w', encoding="utf-8") as outfile:
            geojson.dump(geom_in_geojson, outfile, indent=4, sort_keys=True)
    #return tmp_file[1]
        return HttpResponse("got the json")

    return render(request, 'landuse_manager/Landuse-Manager.html')


def choose(request):
    landuse_directory = "media/landuses"
    file_manager_page_title = "Land Use"
    if not os.path.exists(landuse_directory):
        os.makedirs(landuse_directory)

    landuse_documents = []
    landuse_filelist = os.listdir(landuse_directory)
    for file in landuse_filelist:
        landuse_file = FileManagerDocument()
        landuse_file.doc_name = file
        print("PATH: " + landuse_directory + "/" + file)
        formatted_time = time.strftime('%B %d, %Y', time.gmtime(os.path.getmtime(landuse_directory + "/" + file)))
        landuse_file.date_modified = formatted_time
        landuse_documents.append(landuse_file)

    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        print("BEFORE WENT IN VALID")
        if form.is_valid():
            print("WENT IN VALID")
            newfile = Document()
            newfile.document = form.cleaned_data["docfile"]
            original_name, extension = os.path.splitext(newfile.document.name)
            newfile.document.name = "landuses/" + original_name + extension
            newfile.doc_name = original_name
            newfile.save()
            cleanLandUse(original_name, extension)
            return redirect('landuse_manager:choose')
    else:
        form = DocumentForm()

    context = {
        'form': form,
        'filemanager_filenames': landuse_documents,
        'file_manager_page_title': file_manager_page_title
    }
    return render(request, 'landuse_manager/File-Manager.html', context)

def cleanLandUse(source, srcExtension):
    # ctr = 0
    f = io.open("media/landuses/" + source + "_cleaned.geojson", 'w', encoding="utf-8")
    f.write("{\"type\": \"FeatureCollection\",")
    f.write("\"generator\": \"overpass-turbo\",")
    f.write("\"copyright\": \"The data included in this document is from www.openstreetmap.org. The data is made available under ODbL.\",")
    f.write("\"timestamp\": \"2017-03-19T12:47:02Z\",")
    f.write("\"features\":")
    f.write("[\n")
    ctr = 0
    index = -1
    with open("media/landuses/" + source + srcExtension, encoding="utf-8") as z:
        m = json.load(z)
        print(json.dumps(m))
        for data in m['features']:
            polygon = shape(data['geometry'])
            if polygon.is_valid:
                print("WEW")
                if ctr != 0:
                    f.write(",\n")
                else:
                    ctr = ctr + 1
                index = index + 1
                if 'landuse' not in  data['properties']:
                    data['properties']['landuse'] = "others"
                else:
                    if (data['properties']['landuse'] == "residential"):
                        data['properties']['landuse'] = "residential"
                    elif(data['properties']['landuse'] == "cemetery" or
                    data['properties']['landuse'] == "commercial" or
                    data['properties']['landuse'] == "depot" or
                    data['properties']['landuse'] == "garages" or
                    data['properties']['landuse'] == "port" or
                    data['properties']['landuse'] == "quarry" or
                    data['properties']['landuse'] == "railway" or
                    data['properties']['landuse'] == "retail"):
                        data['properties']['landuse'] = "commercial"
                    elif(data['properties']['landuse'] == "grass" or
                    data['properties']['landuse'] == "forest" or
                    data['properties']['landuse'] == "meadow" or
                    data['properties']['landuse'] == "salt_pond" or
                    data['properties']['landuse'] == "village_green"):
                        data['properties']['landuse'] = "parks"
                    elif( data['properties']['landuse'] == "construction" or
                    data['properties']['landuse'] == "greenfield" or
                    data['properties']['landuse'] == "industrial"):
                        data['properties']['landuse'] = "industrial"
                    elif(data['properties']['landuse'] == "allotment" or
                    data['properties']['landuse'] == "basin" or
                    data['properties']['landuse'] == "brownfield" or
                    data['properties']['landuse'] == "farmland" or
                    data['properties']['landuse'] == "farmyard" or
                    data['properties']['landuse'] == "greenhouse_horticulture" or
                    data['properties']['landuse'] == "orchard" or
                    data['properties']['landuse'] == "pasture" or
                    data['properties']['landuse'] == "peat_cutting" or
                    data['properties']['landuse'] == "plant_nursery" or
                    data['properties']['landuse'] == "reservoir" or
                    data['properties']['landuse'] == "vineyard"):
                        data['properties']['landuse'] = "agriculture"
                    elif(data['properties']['landuse'] == "landfill"):
                        data['properties']['landuse'] = "utilities"
                    elif(data['properties']['landuse'] == "military" or
                    data['properties']['landuse'] == "recreation_ground" or
                    data['properties']['landuse'] == "user defined" or
                    data['properties']['landuse'] == "conservation"):
                        data['properties']['landuse'] = "others"

                f.write("{\"type\": \"Feature\", \"properties\": {")
                f.write("\"id\": \"" + str(index) + "\", ")
                if "name" not in data['properties']:
                    data['properties']['name'] = "no name available"
                f.write("\"name\": \"" + str.replace(data['properties']['name'], '\\', '\\\\')+ "\", ")
                polygon = shapely.geometry.geo.shape(data['geometry'])
                f.write("\"centerlatitude\": \"" + str(polygon.centroid.x) + "\", ")
                f.write("\"centerlongitude\": \"" + str(polygon.centroid.y) + "\", ")
                f.write("\"capacity\": \"200\", ")
                f.write("\"landuse_type\": \"" + data['properties']['landuse'] + "\"},")
                #area here
                f.write("\"geometry\": { \"type\":\"" + data['geometry']['type'] + "\",")
                str_coors = str(data['geometry']['coordinates'])
                f.write("\"coordinates\": " + str(data['geometry']['coordinates'])+ "}")
                f.write("}")
    f.write("\n]")
    f.write("}")
    f.close()
    z.close()
