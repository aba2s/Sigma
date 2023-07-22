from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import *
from django.template import loader

def home(request):
    if request.user.is_authenticated:
        return render(request, 'home.html')
    else:
        msg = 'You are not logged. Please log in first !'
        messages.error(request, msg)
        return redirect('login')

@login_required
def imports(request):
    batchs = BatchName.objects.get(id="00000000-0000-0000-0000-000000000001")
    tasks = batchs.asynchronetask_set.order_by('-start_date')[:8]
    context = {
        'batchs': batchs,
        'tasks': tasks,
        'last_task': tasks.first()
    }
    return render(request, 'imports.html' , context)

def status_details(request):
    return render(request, 'modal.html')

def fetch_task(request, task_id):
    task = get_object_or_404(AsynchroneTask, pk=task_id)
    template = loader.get_template('task.html')
    html = template.render({"task": task}, request)
    data = {
        "finished": task.status != task.INPROGRESS,
        "html": html,
    }
    return JsonResponse(data)