from django.urls import path
from .views import *
from .imports import io_real_spents
from . import insertion_orders
from . import cnt
from . import dsp

urlpatterns = [
    path('', home, name='home'),
    path('imports/', imports, name='imports'),
    # path('modal/', status_details, name='status_details'),
    path('data/', io_real_spents.upload_io_real_spents,
        name='import-consolidated-dsp'),
    path('task/<uuid:task_id>/', fetch_task, name='fetch_task'),
    path('user/<str:pk>/insertion_orders/', insertion_orders.user_insertion_orders,
        name='user_insertion_orders'),
    path('create_user_insertion_order', insertion_orders.create_user_insertion_order,
        name='create_user_insertion_order'),
    path('create_campaign_naming_tool/', cnt.create_campaign_naming_tool,
        name='create_campaign_naming_tool'),
    path('user_campaign_naming_tools/', cnt.user_campaign_naming_tools,
        name='user_campaign_naming_tools'),
    path('insertion_order/<str:pk>/create_user_insertion_order_by_dsp/',
        dsp.create_user_insertion_order_by_dsp, name='create_user_insertion_order_by_dsp'),
    path('insertion_order/<str:pk>/details/',
        insertion_orders.user_insertion_order_details,
        name='user_insertion_order_details'),
    
]
