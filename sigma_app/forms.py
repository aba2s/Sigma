from django import forms
from sigma_app.models import *

# Create custom Date Input
class DateInput(forms.DateInput):
    input_type = 'date'


class UserInsertionOrderForm(forms.ModelForm):
    start_date = forms.DateField(widget=DateInput)
    end_date = forms.DateField(widget=DateInput)

    class Meta:
        model = UserInsertionOrder
        fields = '__all__'
        # exclude = ('user',)
        widgets = {
            'user': forms.Select(
                attrs={
                    'placeholder': 'Select',
                    'class': 'form-control'}
            ),
            'campaign_naming_tool': forms.Select(
                attrs={
                    'placeholder': 'Select',
                    'class': 'form-control'}
            ),
            'budget': forms.TextInput(
                attrs={
                    'placeholder': "Enter Insertion order's budget",
                    'class': 'form-control'}
            ),
            'kpi': forms.Select(
                attrs={'class': 'form-control'}
            ),

            'goal_value': forms.TextInput(
                attrs={
                    'placeholder': "Insertion order's goal",
                    'class': 'form-control'}
            ),
            'start_date': forms.DateInput(
                attrs={
                    'class': 'form-control'}
            ),
        }

    def __init__(self, current_user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # We only want to filter logged user's campaigns
        if current_user:
            queryset = CampaignNamingTool.objects.filter(user=current_user)
            self.fields['campaign_naming_tool'].queryset = queryset


class CampaignNamingToolForm(forms.ModelForm):
    # created_date = forms.DateField(widget=DateInput)

    class Meta:
        model = CampaignNamingTool
        exclude = ('user', 'created_date',)
        widgets = {
            'year': forms.Select(
                attrs={
                    'class': 'form-control'
                }
            ),
            'month': forms.Select(
                attrs={
                    'class': 'form-control'
                }
            ),
            'advertiser': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'device': forms.Select(
                attrs={
                    'class': 'form-control'
                }
            ),
            'type_of_format': forms.Select(
                attrs={
                    'class': 'form-control'
                }
            ),
            'kpi': forms.Select(
                attrs={
                    'class': 'form-control'
                }
            ),

        }


class UploadFileForm(forms.Form):
    file = forms.FileField()


class UserInsertionOrderForm(forms.ModelForm):
    start_date = forms.DateField(widget=DateInput)
    end_date = forms.DateField(widget=DateInput)

    class Meta:
        model = UserInsertionOrder
        fields = '__all__'
        # exclude = ('user',)
        widgets = {
            'user': forms.Select(
                attrs={
                    'placeholder': 'Select',
                    'class': 'form-control'}
            ),
            'campaign_naming_tool': forms.Select(
                attrs={
                    'placeholder': 'Select',
                    'class': 'form-control'}
            ),
            'budget': forms.TextInput(
                attrs={
                    'placeholder': "Enter Insertion order's budget",
                    'class': 'form-control'}
            ),
            'kpi': forms.Select(
                attrs={'class': 'form-control'}
            ),

            'goal_value': forms.TextInput(
                attrs={
                    'placeholder': "Insertion order's goal",
                    'class': 'form-control'}
            ),
            'start_date': forms.DateInput(
                attrs={
                    'class': 'form-control'}
            ),
        }

    def __init__(self, current_user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # We only want to filter logged user's campaigns
        if current_user:
            queryset = CampaignNamingTool.objects.filter(user=current_user)
            self.fields['campaign_naming_tool'].queryset = queryset


class UserInsertionOrderByDspForm(forms.ModelForm):
    start_date = forms.DateField(widget=DateInput)
    end_date = forms.DateField(widget=DateInput)

    class Meta:
        model = UserInsertionOrderByDsp
        fields = '__all__'

    def __init__(self, current_user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if current_user:
            queryset = UserInsertionOrder.objects.filter(user=current_user)
            self.fields['insertion_order'].queryset = queryset

class InsertionOrdersFileForm(forms.Form):
    file = forms.FileField()

