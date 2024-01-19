from django.contrib.auth.models import User
from .models import UserInsertionOrder, UserInsertionOrderByDsp
from .forms import UserInsertionOrderByDspForm
from django.shortcuts import redirect, render


def create_user_insertion_order_by_dsp(request, pk):
    if request.user.is_authenticated:
        current_user = User.objects.get(pk=request.user.id)

    insertion_order = UserInsertionOrder.objects.get(id=pk)
    if request.method == "POST":
        insertion_order = UserInsertionOrderByDsp(insertion_order=insertion_order)
        form = UserInsertionOrderByDspForm(
            request.user, data=request.POST, instance=insertion_order
        )
        if form.is_valid():
            form.save()
            return redirect("user_insertion_orders", pk)
            # return redirect('user_insertion_order_details', pk)

    form = UserInsertionOrderByDspForm(
        request.user,
        initial={
            "insertion_order": insertion_order,
            "user": current_user,
            "start_date": insertion_order.start_date,
            "end_date": insertion_order.end_date,
        },
    )
    context = {"form": form, "insertion_order": insertion_order}
    return render(request, "form.html", context)
