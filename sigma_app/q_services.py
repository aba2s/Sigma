from datetime import timedelta
from .models import AsynchroneTask

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
    asynchrone_task = AsynchroneTask.objects.get(id=task.id)
    asynchrone_task.time_taken = timedelta(seconds=task.time_taken())
    asynchrone_task.result = str(task.result)

    if task.success:
        asynchrone_task.status = AsynchroneTask.SUCCESSED
    else:
        asynchrone_task.status = AsynchroneTask.FAILED

    asynchrone_task.save()