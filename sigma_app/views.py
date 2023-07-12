from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *

def home(request):
    if request.user.is_authenticated:
        return render(request, 'home.html')
    else:
        msg = 'You are not logged. Please log in first !'
        messages.error(request, msg)
        return redirect('login')

def imports(request):
    batchs = BatchName.objects.all()
    context = {
        'batchs': batchs
    }
    return render(request, 'imports.html' , context)

def data_streams(request):
    batchs = [
       {"DSP": "FreWheel", "User": "aba2s", "Status": "Terminé",
        "Valid Count": 20, "Error Count": 5, "Import Date":	"16-04-2023 08:19",
        "File name": "FreeWheel import - 16042023"},
        {"DSP": "FreWheel", "User": "aba2s", "Status": "Terminé",
        "Valid Count": 20, "Error Count": 5, "Import Date":	"16-04-2023 08:19",
        "File name": "FreeWheel import - 16042023"},
        {"DSP": "FreWheel", "User": "aba2s", "Status": "Terminé",
        "Valid Count": 20, "Error Count": 5, "Import Date":	"16-04-2023 08:19",
        "File name": "FreeWheel import - 16042023"},
        {"DSP": "FreWheel", "User": "aba2s", "Status": "Terminé",
        "Valid Count": 20, "Error Count": 5, "Import Date":	"16-04-2023 08:19",
        "File name": "FreeWheel import - 16042023"},
        {"DSP": "FreWheel", "User": "aba2s", "Status": "Terminé",
        "Valid Count": 20, "Error Count": 5, "Import Date":	"16-04-2023 08:19",
        "File name": "FreeWheel import - 16042023"}
    ]
    return render(request, 'imports.html', {"batchs": batchs})

def status_details(request):
    return render(request, 'modal.html')
