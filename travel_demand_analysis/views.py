from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, redirect
import json
import os
import geojson
import os.path, time
from .custom_models.constants import *
from .custom_models.FourStepModel import TripGeneration, TripDistribution
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


    amenity_filenames = [file for file in os.listdir(amenity_directory) if file.endswith('_cleaned.json')]
    household_filenames = os.listdir(household_directory)
    trafficzone_filenames = os.listdir(trafficzone_directory)

    print("FILES: "+str(household_filenames)+":"+str(amenity_filenames)+":"+str(trafficzone_filenames))

    with open('travel_demand_analysis/coors.json', encoding='utf8') as f:
        json_data = json.load(f)

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
        preprocessed_frame, taz_info_preanalysis = trip_analyzer.trip_analyze()
        preprocessed_frame.to_csv("media/PRE_TRIPGEN_FINISHED.csv", encoding='utf-8')
        trip_generation = TripGeneration("media/PRE_TRIPGEN_FINISHED.csv", "trips")

        trip_generation.setProductionParameters(production_attribute_names,
                                                production_attribute_intercept,
                                                production_attribute_coeffiients)
        trip_generation.setAttractionParameters(attraction_attribute_names,
                                                attraction_attribute_intercept,
                                                attraction_attribute_coeffiients)

        df, overall_trip_production, overall_trip_attraction = trip_generation.printAllZonalTripsProductionAttraction()

        td = TripDistribution(overall_trip_production, overall_trip_attraction)
        #distribution = td.getTripDistribution()
        distribution = td.getDummyOD(len(overall_trip_production), len(overall_trip_production))
        pandas_distrib = pd.DataFrame(distribution, columns=range(0, len(overall_trip_production)))
        #zonal_od_matrix = json.dumps(distribution, indent=4)
        #print(" od_matrix: "+str(zonal_od_matrix))

        for index, zone_info in enumerate(taz_info_preanalysis):
            zone_info.trips_produced = overall_trip_production[index]
            zone_info.trips_attracted = overall_trip_attraction[index]

        zone_info_json = json.dumps([ob.__dict__ for ob in taz_info_preanalysis], default=lambda o: o.__dict__,
                                    indent=4, sort_keys=True)
        df.to_csv("media/SAMPLE_ZONAL_PROD_ATTR.csv", encoding='utf-8')
        data = {}
        data['max_trip_produced'] = max(overall_trip_production)
        data['max_trip_attracted'] = max(overall_trip_attraction)
        data['taz_json'] = zone_info_json
        data['zonal_od'] = distribution
        return HttpResponse(json.dumps(data), content_type='application/json')
    return HttpResponse("Non ajax post request")


def analysis_add_amenity(request):
    if request.is_ajax() and request.POST:
        amenity_filename = request.POST.get('amenity_filename')
        file_path = "media/amenities/" + str(amenity_filename)

        with open(file_path, encoding="utf-8") as f:
            json_data = json.load(f)
        amenity_dump = json.dumps(json_data)

        data = {}
        data['no_amenities'] = len(json_data)
        data['amenity_filename'] = amenity_filename
        data['amenities_json'] = amenity_dump


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
