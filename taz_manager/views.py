from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, redirect
import json
from taz_manager.forms import DocumentForm
from taz_manager.models import Document, FileManagerDocument
import os
import os.path, time


def index(request):
    context = {}
    return render(request, 'index.html', context)


def manage(request):
    with open('taz_manager/coors.json', encoding='utf8') as f:
        json_data = json.load(f)

    context = {
        'coordinates_var' : json_data["features"],
    }
    return render(request, 'TAZ-Manager.html', context)


def choose(request):
    trafficzone_directory = "media/trafficzones"
    if not os.path.exists(trafficzone_directory):
        os.makedirs(trafficzone_directory)

    trafficzone_documents = []
    trafficzone_filelist = os.listdir(trafficzone_directory)
    for file in trafficzone_filelist:
        trafficzone_file = FileManagerDocument()
        trafficzone_file.doc_name = file
        print("PATH: " + trafficzone_directory + "/" + file)
        formatted_time = time.strftime('%B %d, %Y', time.gmtime(os.path.getmtime(trafficzone_directory + "/" + file)))
        trafficzone_file.date_modified = formatted_time
        trafficzone_documents.append(trafficzone_file)

    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        print("BEFORE WENT IN VALID")
        if form.is_valid():
            print("WENT IN VALID")
            newfile = Document()
            newfile.document = form.cleaned_data["docfile"]
            original_name, extension = os.path.splitext(newfile.document.name)
            newfile.document.name = "trafficzones/" + original_name + extension
            newfile.doc_name = original_name
            newfile.save()
            return redirect('taz_manager:choose')
    else:
        form = DocumentForm()

    context = {
        'form': form,
        'filemanager_filenames': trafficzone_documents
    }
    return render(request, 'File-Manager.html', context)
