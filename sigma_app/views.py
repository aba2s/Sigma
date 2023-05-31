from django.shortcuts import render


def home(request):
    return render(request, 'home.html')

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
