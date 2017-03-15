from django.shortcuts import render
import json


def index(request):
    context = {}
    return render(request, 'amenities_manager/File-Manager.html', context)


def manage(request):
    with open('amenities_manager/coors.json', encoding='utf8') as f:
        json_data = json.load(f)

    context = {
        'coordinates_var': json_data["features"],
    }
    return render(request, 'amenities_manager/Amenities-Manager.html', context)


def choose(request):
    context = {
    }
    return render(request, 'amenities_manager/File-Manager.html', context)
