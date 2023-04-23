from django.shortcuts import render


def landing_page(request):
    return render(request, 'index.html')

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
    return render(request, 'data_streams.html', {"batchs": batchs})

def status_details(request):
    return render(request, 'modal.html')
