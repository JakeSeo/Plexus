from django.shortcuts import render
import json


def index(request):
    context = {}
    return render(request, 'landuse_manager/index.html', context)


def manage(request):
    with open('landuse_manager/coors.json', encoding='utf8') as f:
        json_data = json.load(f)

    context = {
        'coordinates_var' : json_data["features"],
    }
    return render(request, 'landuse_manager/Landuse-Manager.html', context)


def choose(request):
    context = {
    }
    return render(request, 'landuse_manager/File-Manager.html', context)
