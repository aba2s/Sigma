from datetime import date
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect 
from django.contrib.auth.decorators import login_required
from sigma_app.models import CampaignNamingTool
from sigma_app.filters import CampaignNamingToolFilter
from .filters import *
from .forms import *


@login_required
def user_campaign_naming_tools(request):
    user_campaign_naming_tool = CampaignNamingTool.objects.filter(
        user=request.user).order_by('-created_date')

    # Full text filter
    if request.GET.get('item-to-search'):
        qs = request.GET['item-to-search']
        user_campaign_naming_tool = user_campaign_naming_tool.filter(
            name__icontains=qs)

    # Django FilterSet
    advanced_filter = CampaignNamingToolFilter(
        request.GET, queryset=user_campaign_naming_tool)
    user_campaign_naming_tool_filter = advanced_filter.qs

    context = {
        "cnts": user_campaign_naming_tool_filter,
        'user_cnts_advanced_filter': advanced_filter,
        'user_cnts_full_text_search': user_campaign_naming_tool
    }
    return render(request, 'cnt/cnt.html', context)

@login_required
def create_campaign_naming_tool(request):
    # current_user = User.objects.get(pk=request.user.id)
    # form = CampaignNamingToolForm(initial={'user': current_user})
    form = CampaignNamingToolForm(initial={
        'user': request.user,
        'year': date.today().year,
        'month': "0" + str(date.today().month)
        })
    if request.method == 'POST':
        campaign = CampaignNamingTool(user=request.user)
        form = CampaignNamingToolForm(request.POST, instance=campaign)
        if form.is_valid():
            form.save()
            msg = "«{}» have been successfully created !".format(
                form.instance)
            messages.success(request, msg)
            return redirect('user_campaign_naming_tools')
        else:
            messages.error(request, form.errors['__all__'])
            return render(request, 'form.html', {'form': form})
    
    context = {
        'form': form,
    }
    return render(request, 'form.html', context)