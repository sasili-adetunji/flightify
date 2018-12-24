from celery.decorators import task, periodic_task
from celery.utils.log import get_task_logger
from celery.task.schedules import crontab

from .email_helper import (
    send_signup_confirmation,
    send_ticket_email,
    send_ticket_reminder
)

logger = get_task_logger(__name__)


@task(name="send_signup_email_task")
def send_signup_email_task(user):
    """sends an email when signup form is filled successfully"""

    logger.info("Sent signup email")
    return send_signup_confirmation(user)


@task(name="send_ticket_email_task")
def send_ticket_email_task(result):
    """sends an email when a ticket is booked"""

    logger.info("Sent ticket email")
    return send_ticket_email(result)

@periodic_task(
    run_every=(crontab(minute='*')),
    name="task_send_email_reminder",
    ignore_result=True
)
def task_send_email_reminder():
    """
    Sends email notification to users 24hours before departure
    """

    logger.info("Flight reminder sent")
    return send_ticket_reminder()
