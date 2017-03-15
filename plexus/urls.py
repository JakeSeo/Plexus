
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^amenities_manager/', include('amenities_manager.urls')),
    url(r'^landuse_manager/', include('landuse_manager.urls')),
]
