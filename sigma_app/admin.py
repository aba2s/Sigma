from django.contrib import admin
from .models import CampaignNamingTool
from .models import UserInsertionOrder
from .models import InsertionOrdersRealSpents


# Register your models here.
admin.site.register(CampaignNamingTool)
admin.site.register(UserInsertionOrder)
admin.site.register(InsertionOrdersRealSpents)
