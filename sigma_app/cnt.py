from datetime import date
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import CampaignNamingTool
from .filters import CampaignNamingToolFilter
from .forms import CampaignNamingToolForm
from .forms import UploadFileForm
import csv
import json


@login_required
def user_campaign_naming_tools(request, pk):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=pk)

        user_campaign_naming_tool = CampaignNamingTool.objects.filter(
            user=current_user
        ).order_by("-created_date")

        # Full text filter
        if request.GET.get("item-to-search"):
            qs = request.GET["item-to-search"]
            user_campaign_naming_tool = user_campaign_naming_tool.filter(
                name__icontains=qs
            )

        # Django FilterSet
        advanced_filter = CampaignNamingToolFilter(
            request.GET, queryset=user_campaign_naming_tool
        )
        user_campaign_naming_tool_filter = advanced_filter.qs

        context = {
            "cnts": user_campaign_naming_tool_filter,
            "user_cnts_advanced_filter": advanced_filter,
            "user_cnts_full_text_search": user_campaign_naming_tool,
        }
        return render(request, "cnt/cnt.html", context)


@login_required
def create_campaign_naming_tool(request):
    current_user = User.objects.get(pk=request.user.id)
    form = CampaignNamingToolForm(
        initial={
            # 'user': request.user,
            "user": current_user,
            "year": date.today().year,
            "month": "0" + str(date.today().month),
        }
    )
    if request.method == "POST":
        campaign = CampaignNamingTool(user=request.user)
        form = CampaignNamingToolForm(request.POST, instance=campaign)
        if form.is_valid():
            form.save()
            msg = "«{}» have been successfully created !".format(form.instance)
            return HttpResponse(
                status=204,
                headers={
                    "HX-Trigger": json.dumps(
                        {"InsertionOrderListChanged": None, "showMessage": msg}
                    )
                },
            )
        else:
            # messages.error(request, form.errors['__all__'])
            messages.error(request, form.errors)
            return render(request, "form.html", {"form": form})

    context = {"form": form, "is_create_campaign_naming_tool": True}
    return render(request, "form.html", context)


@login_required
def bulk_create_campaign_naming_tool(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        user_campaign_naming_tool = []
        if form.is_valid():
            file = request.FILES["file"]
            if file.name.endswith(".csv"):
                data_file = (
                    file.read()
                    .decode(encoding="utf-8", errors="ignore")  # \ufeff: utf-8-sig
                    .splitlines()
                )
                data = csv.DictReader(data_file, delimiter=";", quoting=csv.QUOTE_NONE)
                for row in data:
                    campaign_naming_tool_instance = CampaignNamingTool(
                        user=request.user,
                        year=row["year"],
                        month=row["month"],
                        advertiser=row["advertiser"],
                        name=row["name"],
                        device=row.get("device", "Multi-device"),
                        type_of_format=row.get("format", "IAB"),
                        kpi=row.get("kpi", "CPM"),
                    )
                    user_campaign_naming_tool.append(campaign_naming_tool_instance)
                try:
                    CampaignNamingTool.objects.bulk_create(user_campaign_naming_tool)
                except IntegrityError:
                    msg = "Insertion Orders already exist."
                    messages.error(request, msg)
                    return redirect("bulk_create_campaign_naming_tool")
                except Exception as e:
                    messages.error(request, e)
                    return redirect("bulk_create_campaign_naming_tool")
                else:
                    messages.success(request, "success")
                    return redirect("user_campaign_naming_tools", request.user.id)
            else:
                msg = "File format is not recognized.\
                       It must be a csv format !"
                messages.error(request, msg)
            return redirect("user_campaign_naming_tools", request.user.id)
        else:
            messages.error(request, "Form is not valid")
            return redirect("bulk_create_campaign_naming_tool")

    form = UploadFileForm()
    context = {"form": form, "is_create_campaign_naming_tool": True}
    return render(request, "upload.html", context)
