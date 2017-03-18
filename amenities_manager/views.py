from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, redirect
import json
from amenities_manager.forms import DocumentForm
from amenities_manager.models import Document, FileManagerDocument
import os
import os.path, time


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
    amenity_directory = "media/amenities"
    if not os.path.exists(amenity_directory):
        os.makedirs(amenity_directory)

    amenity_documents = []
    amenity_filelist = os.listdir(amenity_directory)
    for file in amenity_filelist:
        amenity_file = FileManagerDocument()
        amenity_file.doc_name = file
        print("PATH: " + amenity_directory + "/" + file)
        formatted_time = time.strftime('%B %d, %Y', time.gmtime(os.path.getmtime(amenity_directory + "/" + file)))
        amenity_file.date_modified = formatted_time
        amenity_documents.append(amenity_file)

    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        print("BEFORE WENT IN VALID")
        if form.is_valid():
            print("WENT IN VALID")
            newfile = Document()
            newfile.document = form.cleaned_data["docfile"]
            original_name, extension = os.path.splitext(newfile.document.name)
            newfile.document.name = "amenities/" + original_name + extension
            newfile.doc_name = original_name
            newfile.save()
            return redirect('amenities_manager:choose')
    else:
        form = DocumentForm()

    context = {
        'form': form,
        'filemanager_filenames': amenity_documents
    }
    return render(request, 'amenities_manager/File-Manager.html', context)
