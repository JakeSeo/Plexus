from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, redirect
import json
from household_manager.forms import DocumentForm
from household_manager.models import Document, FileManagerDocument
import os
import os.path, time


def index(request):
    context = {}
    return render(request, 'household_manager/index.html', context)


def manage(request):
    with open('household_manager/coors.json', encoding='utf8') as f:
        json_data = json.load(f)

    context = {
        'coordinates_var' : json_data["features"],
    }
    return render(request, 'household_manager/Household-Manager.html', context)


def choose(request):
    household_directory = "media/households"
    if not os.path.exists(household_directory):
        os.makedirs(household_directory)

    household_documents = []
    household_filelist = os.listdir(household_directory)
    for file in household_filelist:
        household_file = FileManagerDocument()
        household_file.doc_name = file
        print("PATH: " + household_directory + "/" + file)
        formatted_time = time.strftime('%B %d, %Y', time.gmtime(os.path.getmtime(household_directory + "/" + file)))
        household_file.date_modified = formatted_time
        household_documents.append(household_file)



    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        print("BEFORE WENT IN VALID")
        if form.is_valid():
            print("WENT IN VALID")
            newfile = Document()
            newfile.document = form.cleaned_data["docfile"]
            original_name, extension = os.path.splitext(newfile.document.name)
            newfile.document.name = "households/" + original_name + extension
            newfile.doc_name = original_name
            newfile.save()
            return redirect('file_manager_household')
    else:
        form = DocumentForm()

    context = {
        'form': form,
        'filemanager_filenames': household_documents
    }
    return render(request, 'household_manager/File-Manager.html', context)
