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
from shapely.geometry.polygon import LinearRing, Polygon
from shapely.geometry.multipolygon import MultiPolygon
import geojson
import io


def index(request):
    context = {}
    return render(request, 'landuse_manager/index.html', context)


def manage(request):
    with open('media/landuse/landusegeojson.geojson', encoding="utf-8") as f:
        json_data = json.load(f)
    context = {
        'amenities': json.dumps(json_data)
    }
    return render(request, 'LandUse-Manager.html', context)

def manageSave(request):
    if request.is_ajax() and request.POST:
        data = request.POST.get('landuse')
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
        with open("media/landuse/landuse--edited.geojson", 'w', encoding="utf-8") as outfile:
            geojson.dump(geom_in_geojson, outfile, indent=4, sort_keys=True)
    #return tmp_file[1]
        return HttpResponse("got the json")

    return render(request, 'Landuse-Manager.html')


def choose(request):
    landuse_directory = "media/landuse"
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
    f = io.open("media/landuse/" + source + "_cleaned.geojson", 'w', encoding="utf-8")
    f.write("[\n")
    ctr = 0
    index = -1
    with io.open("media/landuse/" + source + srcExtension, encoding="utf-8") as z:
        m = json.load(z)
        for data in m['features']:
            if ctr != 0:
                f.write(",\n")
            else:
                ctr = ctr + 1
            index = index + 1
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
            f.write("\"geometry\": {\"type\": \"Polygon\",")
            f.write("\"coordinates\": [" + str(data['geometry']['coordinates'])+ "]}")
            f.write("}")
    f.write("\n]")
    f.close()
    z.close()
