from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('data-streams/batchs', data_streams, name='data-streams'),
    path('modal/', status_details, name='status_details')
]
