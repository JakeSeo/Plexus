from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, redirect
import json
from landuse_manager.forms import DocumentForm
from landuse_manager.models import Document, FileManagerDocument
import os
import os.path, time


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
    landuse_directory = "media/landuse"
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
            return redirect('landuse_manager:choose')
    else:
        form = DocumentForm()

    context = {
        'form': form,
        'filemanager_filenames': landuse_documents
    }
    return render(request, 'landuse_manager/File-Manager.html', context)
