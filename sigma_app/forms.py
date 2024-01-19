"""
Here we define all our forms
"""
from django import forms
from .models import UserInsertionOrder
from .models import CampaignNamingTool
from .models import UserInsertionOrderByDsp


# Create custom Date Input
class DateInput(forms.DateInput):
    input_type = "date"


class UploadFileForm(forms.Form):
    file = forms.FileField()


class InsertionOrdersFileForm(forms.Form):
    file = forms.FileField()


class CampaignNamingToolForm(forms.ModelForm):
    # created_date = forms.DateField(widget=DateInput)

    class Meta:
        model = CampaignNamingTool
        fields = [
            "year",
            "month",
            "advertiser",
            "name",
            "device",
            "type_of_format",
            "kpi",
        ]
        widgets = {
            "year": forms.Select(attrs={"class": "form-control"}),
            "month": forms.Select(attrs={"class": "form-control"}),
            "advertiser": forms.TextInput(attrs={"class": "form-control"}),
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "device": forms.Select(attrs={"class": "form-control"}),
            "type_of_format": forms.Select(attrs={"class": "form-control"}),
            "kpi": forms.Select(attrs={"class": "form-control"}),
        }


class UserInsertionOrderForm(forms.ModelForm):
    start_date = forms.DateField(widget=DateInput)
    end_date = forms.DateField(widget=DateInput)

    class Meta:
        model = UserInsertionOrder
        fields = [
            "user",
            "campaign_naming_tool",
            "budget",
            "kpi",
            "goal_value",
            "start_date",
            "end_date",
        ]
        widgets = {
            "user": forms.Select(
                attrs={"placeholder": "Select", "class": "form-control"}
            ),
            "campaign_naming_tool": forms.Select(
                attrs={"placeholder": "Select", "class": "form-control"}
            ),
            "budget": forms.TextInput(
                attrs={
                    "placeholder": "Enter Insertion order's budget",
                    "class": "form-control",
                }
            ),
            "kpi": forms.Select(attrs={"class": "form-control"}),
            "goal_value": forms.TextInput(
                attrs={"placeholder": "Insertion order's goal", "class": "form-control"}
            ),
            "start_date": forms.DateInput(attrs={"class": "form-control"}),
        }

    def __init__(self, current_user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # We only want to filter logged user's campaigns
        if current_user:
            queryset = CampaignNamingTool.objects.filter(user=current_user)
            self.fields["campaign_naming_tool"].queryset = queryset


class UserInsertionOrderByDspForm(forms.ModelForm):
    start_date = forms.DateField(widget=DateInput)
    end_date = forms.DateField(widget=DateInput)

    class Meta:
        model = UserInsertionOrderByDsp
        fields = ["user", "insertion_order", "dsp", "budget", "start_date", "end_date"]

    def __init__(self, current_user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if current_user:
            queryset = UserInsertionOrder.objects.filter(user=current_user)
            self.fields["insertion_order"].queryset = queryset
