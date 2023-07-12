from datetime import date
from django.contrib.auth.models import User
from .filters import *
from .forms import *
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, F, Case, When, DecimalField

@login_required
def user_insertion_orders(request, pk):
    """
    This views filter only the campaigns of the logged users. 
    """
    if request.user.is_authenticated:
        current_user = User.objects.get(id=pk)
        # Get all insertion order related to the current user
        insertion_orders = current_user.userinsertionorder_set.filter(
            user=current_user).order_by('-created_date')
        # The first parameter for FilterSet is data, the second is queryset.
        # So here to display in the drop down only the logged user objects,
        # we have to replace request.GET by request.user (or the current_user)
        # after overriding the in-built __init__ function in the FilterSet.
        
        filter = UserInsertionOrderFilter(
            request.user,
            data=request.GET,
            queryset=insertion_orders
        )
        insertion_orders_filter = filter.qs
        context = {
            'user': current_user,
            'insertion_orders': insertion_orders_filter,
            'filter': filter
        }

        return render(
            request,
            'insertion_orders/insertion_orders.html',
            context)
    else:
        msg = 'You are not logged. Please log in first !'
        messages.error(request, msg)
        return redirect('login')

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

        if request.method == 'POST':
            insertion_order = UserInsertionOrder(user=current_user)
            form = UserInsertionOrderForm(
                request.user,
                data=request.POST,
                instance=insertion_order
            )
            if form.is_valid():
                form.save()
                msg = "«{}» have been successfully created !".format(
                form.instance)
                messages.success(request, msg)
                return redirect('user_insertion_orders', request.user.id)
            else:
                return render(request, 'form.html', {'form': form})
        else:
            form = UserInsertionOrderForm(
            current_user,
            initial={
                'user': current_user
            })

            return render(request, 'form.html', {'form': form})
    else:
        msg = 'You are not logged. Please log in first !'
        messages.error(request, msg)
        return redirect('login')

def user_insertion_order_details(request, pk):

    insertion_order = UserInsertionOrder.objects.get(id=pk)
    insertion_orders_by_dsp = insertion_order.userinsertionorderbydsp_set.all()
    insertion_orders_by_dsp_dict = {
        io.dsp: io.budget for io in insertion_orders_by_dsp
    }

    # Get the insertion order stats (impressions, clicks, spent budget etc)
    # from InsertionOrders models cad from DSP delivery
    insertion_order_delivery = InsertionOrdersRealSpents.objects.filter(
        insertion_order=insertion_order)
    metrics = {
        'spent_budget': Sum('budget'),
        'impressions': Sum('impressions'),
        'clicks': Sum('clicks'),
        'post_clicks_conversions': Sum('post_clicks_conversions'),
        'conversions': Sum('conversions'),
    }
    pivot_table = insertion_order_delivery\
        .values('insertion_order', 'dsp')\
        .annotate(**metrics)\
        .annotate(
            click_rate=Case(
                When(impressions=0, then=0),
                default=F('clicks') / F('impressions'),
                output_field=DecimalField(decimal_places=2)
            ),
            arrival_rate=Case(
                When(clicks=0, then=0),
                default=F('post_clicks_conversions') / F('clicks'),
                output_field=DecimalField(decimal_places=2)
            )
        )

    # Adding dsp budget in InsertionOrders(delivery) dictionary
    for dictionary in pivot_table:
        budget = insertion_orders_by_dsp_dict.get(dictionary['dsp'])
        dictionary['budget'] = budget
        try:
            dictionary['delivery'] = dictionary['spent_budget'] / budget * 100
        except TypeError:  # In case the user didn't register the campaign yet
            dictionary['delivery'] = 0

    total_aggreation = insertion_order_delivery.aggregate(**metrics)
    try:
        delivery_rate = total_aggreation['spent_budget'] / \
            insertion_order.budget * 100
    except TypeError:
        delivery_rate = 0

    number_of_date = date.today() - insertion_order.start_date
    insertion_order_period = \
        insertion_order.end_date - insertion_order.start_date
    theorical_delivery = (number_of_date.days + 1) / \
        (insertion_order_period.days + 1) * 100

    context = {
        'insertion_order': insertion_order,
        'insertion_orders_by_dsp_dict': insertion_orders_by_dsp_dict,
        'total': total_aggreation,
        'delivery_rate': delivery_rate,
        'theorical_delivery': theorical_delivery,
        'pivot_table': pivot_table
    }

    return render(request, 'insertion_orders/details.html', context)