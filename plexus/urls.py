
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^amenities_manager/', include('amenities_manager.urls')),
    url(r'^landuse_manager/', include('landuse_manager.urls')),
    url(r'^household_manager/', include('household_manager.urls')),
    url(r'^travel_demand_analysis/', include('travel_demand_analysis.urls')),
    url(r'^taz_manager/', include('taz_manager.urls'))
]
