import geojson
from geojson import Feature, Polygon, FeatureCollection
import json
import pygeoj
import io
from shapely.geometry import shape, Point
import pandas as pd
# from models.taz import TAZ

class TAZ:
    def __init__(self):
        self.zone_polygon = None
        self.trips = 0
        self.no_hh = 0
        self.no_mem = 0
        self.no_mem_educ = 0
        self.no_mem_work = 0
        self.total_income = 0
        self.no_amty_sustenance = 0
        self.no_amty_education = 0
        self.no_amty_transport = 0
        self.no_amty_healthcare = 0
        self.no_amty_finance = 0
        self.no_amty_commerce = 0
        self.no_amty_entertainment = 0
        self.no_amty_other = 0
        self.lu_ind_commercial = 0
        self.lu_ind_parks = 0
        self.lu_ind_industrial = 0
        self.lu_ind_agriculture = 0
        self.lu_ind_residential = 0
        self.lu_ind_utilities = 0
   
    def __str__(self):
        return "no_hh:"+str(self.no_hh)+" no_mem:"+str(self.no_mem)+" total_income:"+str(self.total_income)
    
    def get_attr_vals(self):
        if(self.no_hh>0):
            self.total_income = self.total_income/self.no_hh
        return [self.trips, self.no_hh, self.no_mem, self.no_mem_educ, self.no_mem_work, self.total_income, 
                self.no_amty_sustenance, self.no_amty_education, self.no_amty_transport, self.no_amty_healthcare,
                self.no_amty_finance, self.no_amty_commerce, self.no_amty_entertainment, self.no_amty_other,
                self.lu_ind_commercial, self.lu_ind_parks, self.lu_ind_industrial, self.lu_ind_agriculture,
                self.lu_ind_residential, self.lu_ind_utilities]

class TripAnalyzer:
    def __init__(self, taz_geo_files, cbms_files, amenity_files, zone_landuse_setting):
        self.traffic_analysis_zones = []
        
        self.taz_geo_files = taz_geo_files
        self.cbms_files = cbms_files
        self.amenity_files = amenity_files
        self.zone_landuse_setting = zone_landuse_setting
    
    
    def trip_analyze(self):
        for file in self.taz_geo_files:
            #geofile = pygeoj.load("MetropolitantManila.geojson")
            geofile = pygeoj.load("media/trafficzones/"+str(file))
            for feature in geofile:
                polygon = shape(feature.geometry)
                raw_taz = TAZ()
                raw_taz.zone_polygon = polygon
                self.traffic_analysis_zones.append(raw_taz)
                
        #Loop through all cbms files pa
        for file in self.cbms_files:
            with io.open("media/households/"+str(file), encoding="utf-8") as z:
                for line in z:
                    #print(line)
                    data = json.loads(line, strict=False)
                    hh_lat, hh_long = data['latitude'], data['longitude']
                    #print(str(hh_lat)+","+str(hh_long)+": "+str(hh_lat is not str(0))+"!"+str(hh_long is not str(0)))
                    if not(hh_lat == "0" and hh_long == "0"):
                        point = Point(float(hh_long),float(hh_lat))
                        for index, zone in enumerate(self.traffic_analysis_zones):
                            if zone.zone_polygon.contains(point):
                                #traffic_analysis_zones[index] = TAZ()
                                zone.no_hh = zone.no_hh + 1
                                zone.no_mem = zone.no_mem + int(data['phsize'])
                                zone.no_mem_educ = zone.no_mem_educ + int(data['toteduc'])
                                zone.no_mem_work = zone.no_mem_work + int(data['totjob'])
                                zone.total_income = zone.total_income + float(data['totin'])
                                #print("Update Zone["+str(index)+"]: "+str(zone))
                 
        #Populate Amenity attributes
        for file in self.amenity_files:
            with open("media/amenities/"+str(file), encoding="utf-8") as json_data:
                json_elems = json.load(json_data)

            for json_obj in json_elems:
                am_lat, am_long = json_obj['latitude'], json_obj['long']
                if am_lat == "0" and am_long == "0":
                    print(line)
                else:
                    point = Point(float(am_long), float(am_lat))
                    # print(point)
                    for index, zone in enumerate(self.traffic_analysis_zones):
                        if zone.zone_polygon.contains(point):
                            amenity_type = json_obj['amenity_type']
                            if amenity_type == "sustenance":
                                zone.no_amty_sustenance = zone.no_amty_sustenance + 1
                            elif amenity_type == "education":
                                zone.no_amty_education = zone.no_amty_education + 1
                            elif amenity_type == "transport":
                                zone.no_amty_transport = zone.no_amty_transport + 1
                            elif amenity_type == "healthcare":
                                zone.no_amty_healthcare = zone.no_amty_healthcare + 1
                            elif amenity_type == "finance":
                                zone.no_amty_finance = zone.no_amty_finance + 1
                            elif amenity_type == "commerce":
                                zone.no_amty_commerce = zone.no_amty_commerce + 1
                            elif amenity_type == "entertainment":
                                zone.no_amty_entertainment = zone.no_amty_entertainment + 1
                            elif amenity_type == "other":
                                zone.no_amty_other = zone.no_amty_other + 1

        for index, landuse in enumerate(self.zone_landuse_setting):
            if(landuse == "commercial"):
                print("went1")
                self.traffic_analysis_zones[index].lu_ind_commercial = 1
            elif(landuse == "parks"):
                print("went2")
                self.traffic_analysis_zones[index].lu_ind_parks = 1
            elif(landuse == "industrial"):
                print("went3")
                self.traffic_analysis_zones[index].lu_ind_industrial = 1
            elif(landuse == "agriculture"):
                print("went4")
                self.traffic_analysis_zones[index].lu_ind_agriculture = 1
            elif(landuse == "residential"):
                print("went5")
                self.traffic_analysis_zones[index].lu_ind_residential = 1
            elif(landuse == "utilities"):
                print("went6")
                self.traffic_analysis_zones[index].lu_ind_utilities = 1
           
        cols = ['trips','no_hh','no_mem','no_mem_educ','no_mem_work','avg_income','no_amty_sustenance',
                'no_amty_education','no_amty_transport','no_amty_healthcare','no_amty_finance',
                'no_amty_commerce','no_amty_entertainment','no_amty_other','lu_ind_commercial',
                'lu_ind_parks', 'lu_ind_industrial', 'lu_ind_agriculture','lu_ind_residential',
                'lu_ind_utilities']
    
        pre_tripgen_table = pd.DataFrame(columns=cols) 
            
        for index, zone in enumerate(self.traffic_analysis_zones):
            pre_tripgen_table.loc[index] = zone.get_attr_vals()
            
        return pre_tripgen_table
        