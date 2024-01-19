from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import BatchName
from .models import AsynchroneTask
from django.template import loader


def home(request):
    if request.user.is_authenticated:
        return render(request, "home.html")
    else:
        return render(request, "hp/index.html")


@login_required
def imports(request):
    """Batch or datastream"""
    # batch = BatchName.objects.get(id="00000000-0000-0000-0000-000000000001")
    batchs = BatchName.objects.all()

    tasks_dict = {}
    for batch in batchs:
        batch_asynchrone_tasks = batch.asynchronetask_set.order_by("-start_date")[:8]
        tasks_dict.update({batch: batch_asynchrone_tasks})
        
    context = {
        "batchs": batchs,
        "tasks": tasks_dict,
    }
    return render(request, "imports.html", context)


def status_details(request):
    return render(request, "modal.html")


def fetch_task(request, task_id):
    task = get_object_or_404(AsynchroneTask, pk=task_id)
    template = loader.get_template("task.html")
    html = template.render({"task": task}, request)
    data = {
        "finished": task.status != task.INPROGRESS,
        "html": html,
    }
    return JsonResponse(data)


def documentation(request):
    return render(request, "docs/build/html/index.html")
