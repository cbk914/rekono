import os
import signal

from django.core.exceptions import ValidationError
from django.utils import timezone
from executions.models import Execution
from queues.utils import cancel_and_delete_job, cancel_job
from tasks.enums import Status
from tasks.models import Task


def cancel_task(task: Task) -> None:
    '''Cancel task and all his related executions.

    Args:
        task (Task): Task to cancel

    Raises:
        ValidationError: Raised if task can't be cancelled due to his situation
    '''
    if (
        task.status != Status.CANCELLED and                                     # Task status can't be already cancelled
        # Task status can be requested or running or it can be a periodic task
        (task.status in [Status.REQUESTED, Status.RUNNING] or (task.repeat_in and task.repeat_time_unit))
    ):
        if task.rq_job_id:
            # Job Id exists, so it has been enqueued at least one time
            cancel_and_delete_job('tasks-queue', task.rq_job_id)                # Cancel and delete the task job
        # Get all pending executions for this task
        executions = Execution.objects.filter(task=task, status__in=[Status.REQUESTED, Status.RUNNING]).all()
        for execution in executions:                                            # For each execution
            if execution.rq_job_id:                                             # Job Id exists, so it has been enqueued
                cancel_job('executions-queue', execution.rq_job_id)             # Cancel execution job
            if execution.rq_job_pid:
                # Process PID exists, so it is running right now
                os.kill(execution.rq_job_pid, signal.SIGKILL)                   # Kill running process (requires sudo)
            execution.status = Status.CANCELLED                                 # Set execution status to Cancelled
            execution.end = timezone.now()                                      # Update execution end date
            execution.save(update_fields=['status', 'end'])
        task.status = Status.CANCELLED                                          # Set task status to Cancelled
        task.end = timezone.now()                                               # Update task end date
        task.save(update_fields=['status', 'end'])
    else:
        raise ValidationError({'id': f'Task {task.id} can not be cancelled'})   # Task is not eligible for cancellation
