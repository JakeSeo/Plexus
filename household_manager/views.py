from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, redirect
import json
from household_manager.forms import DocumentForm
from household_manager.models import Document, FileManagerDocument
import os
import os.path, time
import io

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
            cleanHH(original_name)
            return redirect('household_manager:choose')
    else:
        form = DocumentForm()

    context = {
        'form': form,
        'filemanager_filenames': household_documents
    }
    return render(request, 'household_manager/File-Manager.html', context)

def cleanHH(source):
    f = io.open("media/households/" + source + "_cleaned.json", 'w', encoding="utf-8")
    f.write("[\n")
    ctr = 0
    index = -1
    with io.open("media/households/" + source + ".json", encoding="utf-8") as z:
        for line in z:
            data = json.loads(line)
            if ctr != 0:
                f.write(",\n")
            else:
                ctr = ctr + 1
            index = index + 1
            f.write("{\"id\":\"")
            f.write(data['_id']['$oid'])
            f.write("\", \"latitude\":\"")
            if data['geopoint_hh']['latitude'] is None or data['geopoint_hh']['latitude'] is "":
                f.write(str(0))
            else:
                f.write(data['geopoint_hh']['latitude'])
            f.write("\", \"longitude\":\"")
            if data['geopoint_hh']['longitude'] is None or data['geopoint_hh']['longitude'] is "":
                f.write(str(0))
            else:
                f.write(data['geopoint_hh']['longitude'])
            f.write("\", \"phsize\":\"")
            if data['phsize'] is None:
                f.write(str(0))
            else:
                f.write(str(data['phsize']))
            f.write("\", \"car\":\"")
            if data['car'] is None:
                f.write(str(0))
            else:
                f.write(str(data['car']))
            f.write("\", \"motor\":\"")
            if data['motor'] is None:
                f.write(str(0))
            else:
                f.write(str(data['motor']))
            f.write("\", \"landagri\":\"")
            if data['landagri'] is None:
                f.write(str(0))
            else:
                f.write(str(data['landagri']))
            f.write("\", \"landres\":\"")
            if data['landres'] is None:
                f.write(str(0))
            else:
                f.write(str(data['landres']))
            f.write("\", \"landcomm\":\"")
            if data['landcomm'] is None:
                f.write(str(0))
            else:
                f.write(str(data['landcomm']))
            f.write("\", \"salind\":\"")
            if data['salind'] is None:
                f.write(str(0))
            else:
                f.write(data['salind'])
            f.write("\", \"servind\":\"")
            if data['servind'] is None:
                f.write(str(0))
            else:
                f.write(data['servind'])
            f.write("\", \"trnind\":\"")
            if data['trnind'] is None:
                f.write(str(0))
            else:
                f.write(data['trnind'])
            f.write("\", \"minind\":\"")
            if data['minind'] is None:
                f.write(str(0))
            else:
                f.write(data['minind'])
            f.write("\", \"totin\":\"")
            if data['totin'] is None:
                f.write(str(0))
            else:
                f.write(str(data['totin']))
            educind = 0
            jobind = 0
            fjob = 0
            for x in data['hpq_mem']:
                if x['educind'] is '1':
                    educind = educind + 1
                if x['jobind'] is '1':
                    jobind = jobind + 1
                if x['fjob'] is '1':
                    fjob = fjob + 1
            f.write("\", \"toteduc\":\"")
            f.write(str(educind))
            f.write("\", \"totjob\":\"")
            f.write(str(jobind))
            f.write("\", \"totfjob\":\"")
            f.write(str(fjob))
            f.write("\"}")
    f.write("\n]")
    f.close()
    z.close()