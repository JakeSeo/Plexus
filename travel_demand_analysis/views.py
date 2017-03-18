from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, redirect
import json
import os
import pygeoj
import geojson
import os.path, time
from .custom_models.constants import *
from .custom_models.FourStepModel import TripGeneration
from .custom_models.TravelAnalyzing import TripAnalyzer
import pandas as pd


def travel_analysis(request):
    amenity_directory = "media/amenities"
    household_directory = "media/households"
    trafficzone_directory = "media/trafficzones"
    if not os.path.exists(amenity_directory):
        print("MAKE DIR1")
        os.makedirs(amenity_directory)
    if not os.path.exists(household_directory):
        print("MAKE DIR2")
        os.makedirs(household_directory)
    if not os.path.exists(trafficzone_directory):
        print("MAKE DIR3")
        os.makedirs(trafficzone_directory)

    amenity_filenames = os.listdir(amenity_directory)
    for file in amenity_filenames:
        if not file.endswith("_cleaned.json"):
            amenity_filenames.remove(file)

    household_filenames = os.listdir(household_directory)
    trafficzone_filenames = os.listdir(trafficzone_directory)

    print("FILES: "+str(household_filenames)+":"+str(amenity_filenames)+":"+str(trafficzone_filenames))

    with open('travel_demand_analysis/coors.json', encoding='utf8') as f:
        json_data = json.load(f)

    # if request.method == 'POST':
    #     form = DocumentForm(request.POST, request.FILES)
    #     if form.is_valid():
    #         newfile = Document()
    #         newfile.doc_name = form.cleaned_data["name"]
    #         newfile.document = form.cleaned_data["docfile"]
    #         original_name, extension = os.path.splitext(newfile.document.name)
    #         newfile.document.name = "tryc/" + form.cleaned_data["name"] + extension
    #         newfile.save()
    #         return redirect('mapdemo2')
    # else:
    #     form = DocumentForm()
    return render(request, 'Analysis.html', {
        'coordinates_var': json_data["features"],
        'amenity_filenames': amenity_filenames,
        'household_filenames': household_filenames,
        'trafficzone_filenames': trafficzone_filenames
    })


def run_analysis(request):
    if request.is_ajax() and request.POST:
        amenity_files = request.POST.getlist('amenity_files[]')
        household_files = request.POST.getlist('household_files[]')
        trafficzone_files = request.POST.getlist('trafficzone_files[]')
        zone_landuse_settings = request.POST.getlist('zone_landuse_settings[]')
        trip_analyzer = TripAnalyzer(trafficzone_files, household_files, amenity_files, zone_landuse_settings)
        preprocessed_frame = trip_analyzer.trip_analyze()
        preprocessed_frame.to_csv("media/PRE_TRIPGEN_FINISHED.csv", encoding='utf-8')
        data = pd.read_csv("media/PRE_TRIPGEN_FINISHED.csv", encoding="utf-8")
        trip_generation = TripGeneration("media/PRE_TRIPGEN_FINISHED.csv", "trips")

        trip_generation.setProductionParameters(production_attribute_names,
                                                production_attribute_intercept,
                                                production_attribute_coeffiients)
        trip_generation.setAttractionParameters(attraction_attribute_names,
                                                attraction_attribute_intercept,
                                                attraction_attribute_coeffiients)

        df, overall_trip_production, overall_trip_attraction = trip_generation.printAllZonalTripsProductionAttraction()
        print("Sample prod, attr:" + str(overall_trip_production) + " " + str(overall_trip_attraction))
        df.to_csv("media/SAMPLE_ZONAL_PROD_ATTR.csv", encoding='utf-8')

        data = {}
        data['overall_trip_production'] = overall_trip_production
        data['overall_trip_attraction'] = overall_trip_attraction

        return HttpResponse(json.dumps(data), content_type='application/json')
    return HttpResponse("Non ajax post request")


def analysis_add_amenity(request):
    if request.is_ajax() and request.POST:
        amenity_filename = request.POST.get('amenity_filename')
        file_path = "media/amenities/" + str(amenity_filename)
        num_lines = 0
        for line in open(file_path, encoding="utf-8").readlines(): num_lines = num_lines + 1
        data = {}
        data['no_amenities'] = num_lines
        data['amenity_filename'] = amenity_filename
        return HttpResponse(json.dumps(data), content_type='application/json')
    return HttpResponse("Non ajax post request")

def analysis_add_household(request):
    if request.is_ajax() and request.POST:
        household_filename = request.POST.get('household_filename')
        file_path = "media/households/" + str(household_filename)

        num_lines = 0
        for line in open(file_path, encoding="utf-8").readlines(): num_lines += 1

        data = {}
        data['no_households'] = num_lines
        data['household_filename'] = household_filename
        return HttpResponse(json.dumps(data), content_type='application/json')
    return HttpResponse("Non ajax post request")


def analysis_add_trafficzone(request):
    if request.is_ajax() and request.POST:
        trafficzone_filename = request.POST.get('trafficzone_filename')
        file_path = "media/trafficzones/" + str(trafficzone_filename)

        geofile = pygeoj.load(file_path)
        zone_tally = 0
        for feature in geofile:
            zone_tally = zone_tally + 1

        data = {}
        data['no_trafficzones'] = zone_tally
        data['trafficzone_filename'] = trafficzone_filename
        data['zone_geojson'] = geojson.dumps(geofile)
        return HttpResponse(json.dumps(data), content_type='application/json')
    return HttpResponse("Non ajax post request")
