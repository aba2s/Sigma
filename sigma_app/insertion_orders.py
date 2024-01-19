import csv
import json
from datetime import date
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, F, Case, When, DecimalField
from .filters import UserInsertionOrderFilter
from .forms import UserInsertionOrderForm
from .forms import UploadFileForm
from .models import InsertionOrdersRealSpents
from .models import UserInsertionOrder
from .models import CampaignNamingTool


@login_required
def user_insertion_orders(request, pk):
    """
    This views filter only the campaigns of the logged users.
    """
    if request.user.is_authenticated:
        current_user = User.objects.get(id=pk)
        # Get all insertion orders related to the current user
        insertion_orders = current_user.userinsertionorder_set.filter(
            user=current_user
        ).order_by("-created_date")
        # The first parameter for FilterSet is data, the second is queryset.
        # So here to display in the drop down only the logged user objects,
        # we have to replace request.GET by request.user (or the current_user)
        # after overriding the in-built __init__ function in the FilterSet.

        filter = UserInsertionOrderFilter(
            request.user, data=request.GET, queryset=insertion_orders
        )
        insertion_orders_filter = filter.qs
        context = {
            "user": current_user,
            "insertion_orders": insertion_orders_filter,
            "filter": filter,
        }

        return render(request, "insertion_orders/insertion_orders.html", context)
    else:
        msg = "You are not logged. Please log in first !"
        messages.error(request, msg)
        return redirect("login")


@login_required
def create_user_insertion_order(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(pk=request.user.id)
        #  Making Model's FK Dropdown Display Current User's CNT Only vs
        # displaying all users's CNT, we have to put request.user before
        # the inializing parameter.
        # That means now the ProductForm has a mandatory
        # parameter in its constructor.
        # So, instead of initializing the form as
        # form = UserInsertionOrderForm(),
        # you need to pass a user instance: form = UserInsertionOrderForm(user)
        # form = UserInsertionOrderForm(initial={'user': current_user})

        if request.method == "POST":
            insertion_order = UserInsertionOrder(user=current_user)
            form = UserInsertionOrderForm(
                request.user, data=request.POST, instance=insertion_order
            )
            if form.is_valid():
                form.save()
                msg = "«{}» have been successfully created !".format(form.instance)
                # messages.success(request, msg)
                # return redirect('user_insertion_orders', request.user.id)
                return HttpResponse(
                    status=204,
                    headers={
                        "HX-Trigger": json.dumps(
                            {"InsertionOrderListChanged": True, "showMessage": msg}
                        )
                    },
                )
            else:
                return render(request, "form.html", {"form": form})

        form = UserInsertionOrderForm(current_user, initial={"user": current_user})
        context = {"form": form, "is_create_user_insertion_order": True}
        return render(request, "form.html", context)
    else:
        msg = "You are not logged. Please log in first !"
        messages.error(request, msg)
        return redirect("login")


def user_insertion_order_details(request, pk):
    insertion_order = UserInsertionOrder.objects.get(id=pk)
    insertion_orders_by_dsp = insertion_order.userinsertionorderbydsp_set.all()
    insertion_orders_by_dsp_dict = {io.dsp: io.budget for io in insertion_orders_by_dsp}

    # Get the insertion order stats (impressions, clicks, spent budget etc)
    # from InsertionOrders models cad from DSP delivery
    insertion_order_delivery = InsertionOrdersRealSpents.objects.filter(
        insertion_order=insertion_order
    )
    metrics = {
        "spent_budget": Sum("budget"),
        "impressions": Sum("impressions"),
        "clicks": Sum("clicks"),
        "post_clicks_conversions": Sum("post_clicks_conversions"),
        "conversions": Sum("conversions"),
    }
    pivot_table = (
        insertion_order_delivery.values("insertion_order", "dsp")
        .annotate(**metrics)
        .annotate(
            click_rate=Case(
                When(impressions=0, then=0),
                default=F("clicks") / F("impressions"),
                output_field=DecimalField(decimal_places=2),
            ),
            arrival_rate=Case(
                When(clicks=0, then=0),
                default=F("post_clicks_conversions") / F("clicks"),
                output_field=DecimalField(decimal_places=2),
            ),
        )
    )

    # Adding dsp budget in InsertionOrders(delivery) dictionary
    for dictionary in pivot_table:
        budget = insertion_orders_by_dsp_dict.get(dictionary["dsp"])
        dictionary["budget"] = budget
        try:
            dictionary["delivery"] = dictionary["spent_budget"] / budget * 100
        except TypeError:  # In case the user didn't register the campaign yet
            dictionary["delivery"] = 0

    total_aggreation = insertion_order_delivery.aggregate(**metrics)
    try:
        delivery_rate = total_aggreation["spent_budget"] / insertion_order.budget * 100
    except TypeError:
        delivery_rate = 0

    number_of_date = date.today() - insertion_order.start_date
    insertion_order_period = insertion_order.end_date - insertion_order.start_date
    theorical_delivery = (
        (number_of_date.days + 1) / (insertion_order_period.days + 1) * 100
    )

    context = {
        "insertion_order": insertion_order,
        "insertion_orders_by_dsp_dict": insertion_orders_by_dsp_dict,
        "total": total_aggreation,
        "delivery_rate": delivery_rate,
        "theorical_delivery": theorical_delivery,
        "pivot_table": pivot_table,
    }

    return render(request, "insertion_orders/details.html", context)


def bulk_create_user_insertion_order(request):
    if request.method == "POST":
        current_user = request.user
        cnts = CampaignNamingTool.objects.filter(user=current_user)
        cnts_instance_dict = {cnt.__str__(): cnt for cnt in cnts}
        print(cnts_instance_dict)
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES["file"]
            if file.name.endswith(".csv"):
                data_file = (
                    file.read().decode(encoding="utf-8", errors="ignore").splitlines()
                )
                data = csv.DictReader(data_file, delimiter=";", quoting=csv.QUOTE_NONE)
                user_insertion_orders_list = list()
                for row in data:
                    try:
                        cnt = cnts_instance_dict[row["insertion_order"]]
                    except KeyError:
                        pass
                    else:
                        kpi = str(cnt).split("-")[-1]
                        user_insertion_order_instance = UserInsertionOrder(
                            user=current_user,
                            campaign_naming_tool=cnt,
                            budget=row["budget"],
                            kpi=kpi,
                            goal_value=row["goal_value"],
                            start_date=row["start_date"],
                            end_date=row["end_date"],
                        )
                        user_insertion_orders_list.append(user_insertion_order_instance)

                try:
                    UserInsertionOrder.objects.bulk_create(user_insertion_orders_list)
                except IntegrityError:
                    msg = "Insertion Orders already exist"
                    messages.warning(request, msg)
                    return redirect("bulk_create_user_insertion_order")
                else:
                    msg = "Insertion orders successfully uploaded"
                    messages.success(request, msg)
                    return redirect("user_insertion_orders", current_user.pk)

            else:
                msg = "File format is not recognized.\
                       It must be a csv format !"
                messages.error(request, msg)
                return redirect("bulk_create_user_insertion_order")

    form = UploadFileForm()
    context = {"form": form, "is_create_campaign_naming_tool": True}
    return render(request, "upload.html", context)
