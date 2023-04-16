from django.shortcuts import render


def landing_page(request):
    return render(request, 'index.html')

def data_streams(request):
    return render(request, 'data_streams.html')
