from datetime import timedelta
from .models import AsynchroneTask
from django_q.models import Task

"""
This module is about django-q services. It will
contain all the functions required by async_task().

We will need to import the async_task function. It takes 3 arguments:
    * The function you want to offload.
    * The arguments you want to pass into the offloaded function.
    * The function you want to run after the worker executes the
      jobin the job queue is hook(); this function takes in task as an argument.
"""

def str_hook(task):
    """Hook for async task that return a string."""
    # Get task from django_q_task table (Task model)
    # django_q_task = Task.objects.get(id=task.id.hex)
    print("#####################################")
    print("Hook starting")
    print("#####################################")
    asynchrone_task = AsynchroneTask.objects.get(id=task.id)
    if not asynchrone_task:
        asynchrone_task.id = task.id
    asynchrone_task.time_taken = timedelta(seconds=task.time_taken())
    asynchrone_task.result = str(task.result)
    # asynchrone_task.task_id = django_q_task

    if task.success:
        asynchrone_task.status = AsynchroneTask.SUCCESSED
        # Get file number of rows and valid rows ingested in database
        res = [int(i) for i in str(task.result).split() if i.isdigit()]
        asynchrone_task.total_rows = res[0]
        asynchrone_task.valid_rows = res[1] 
    else:
        asynchrone_task.status = AsynchroneTask.FAILED
        asynchrone_task.total_rows = 0
        asynchrone_task.valid_rows = 0
    asynchrone_task.save()