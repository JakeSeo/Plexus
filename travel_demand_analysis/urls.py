from django.conf.urls import url
from . import views

app_name = 'travel_demand_analysis'
urlpatterns = [
    url(r'^$', views.travel_analysis, name="travel_analysis"),
    url(r'^run_analysis/$', views.run_analysis, name="run_analysis"),
    url(r'^get_amenity_file/$', views.analysis_add_amenity, name="analysis_add_amenity"),
    url(r'^get_household_file/$', views.analysis_add_household, name="analysis_add_household"),
    url(r'^get_trafficzone_file/$', views.analysis_add_trafficzone, name="analysis_add_trafficzone"),
    url(r'^get_landuse_file/$', views.analysis_add_landuse, name="analysis_add_landuse"),
]
