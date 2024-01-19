from django.urls import path
from .views import fetch_task
from .views import imports
from .views import home
from .views import documentation
from .imports import io_real_spents
from .imports import dsp_spents
from . import insertion_orders
from . import cnt
from . import dsp


urlpatterns = [
    path("", home, name="home"),
    path("documentation/", documentation, name="docs"),
    path("imports/", imports, name="imports"),
    # path("data/", io_real_spents.upload_io_real_spents, name="import-consolidated-dsp"),
    path("data/<str:pk>/", dsp_spents.upload_dsp_spents, name="import-dsp-spents"),
    # path("data/<str:pk>/", dsp_spents.task_upload_dsp_spents, name="import-consolidated-dsp"),
    # path('task/<uuid:task_id>/', fetch_task, name='fetch_task'),
    path("task/<str:task_id>/", fetch_task, name="fetch_task"),
    path(
        "user/<str:pk>/insertion_orders/list/",
        insertion_orders.user_insertion_orders,
        name="user_insertion_orders",
    ),
    path(
        "create_user_insertion_order",
        insertion_orders.create_user_insertion_order,
        name="create_user_insertion_order",
    ),
    path(
        "bulk_create_user_insertion_order/",
        insertion_orders.bulk_create_user_insertion_order,
        name="bulk_create_user_insertion_order",
    ),
    path(
        "create_campaign_naming_tool/",
        cnt.create_campaign_naming_tool,
        name="create_campaign_naming_tool",
    ),
    path(
        "bulk_create_campaign_naming_tool/",
        cnt.bulk_create_campaign_naming_tool,
        name="bulk_create_campaign_naming_tool",
    ),
    path(
        "user/<str:pk>/campaign_naming_tools/list/",
        cnt.user_campaign_naming_tools,
        name="user_campaign_naming_tools",
    ),
    path(
        "insertion_order/<str:pk>/create_user_insertion_order_by_dsp/",
        dsp.create_user_insertion_order_by_dsp,
        name="create_user_insertion_order_by_dsp",
    ),
    path(
        "insertion_order/<str:pk>/details/",
        insertion_orders.user_insertion_order_details,
        name="user_insertion_order_details",
    ),
]
