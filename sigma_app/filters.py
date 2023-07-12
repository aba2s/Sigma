import django_filters
from django_filters import DateFilter, CharFilter
from django import forms
from sigma_app.models import *

# Create custom Date Input
class DateInput(forms.DateInput):
    input_type = 'date'


class UserInsertionOrderFilter(django_filters.FilterSet):
    start_date = django_filters.DateFilter(widget=DateInput)
    end_date = django_filters.DateFilter(widget=DateInput)

    class Meta:
        model = UserInsertionOrder
        fields = [
            'campaign_naming_tool',
            'start_date',
            'end_date'
        ]

    def __init__(self, current_user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if current_user:
            queryset = CampaignNamingTool.objects.filter(user=current_user)
            self.filters['campaign_naming_tool'].queryset = queryset


class CampaignNamingToolFilter(django_filters.FilterSet):
    created_date = DateFilter(
        field_name='created_date',
        lookup_expr='gte',
        label='',
        widget=forms.DateInput(attrs={
            'placeholder': 'tesr',
            'type': 'date',
            'class': 'form-control',
        }))
    name = CharFilter(
        field_name='name',
        lookup_expr='icontains',
        label='',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': "Campaign's name contains",
        })
    )
    advertiser = CharFilter(
        field_name='advertiser',
        lookup_expr='icontains',
        label='',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': "Advertiser's name contains",
        })
    )

    class Meta:
        model = CampaignNamingTool
        fields = [
            'name',
            'advertiser',
            'created_date',
        ]

