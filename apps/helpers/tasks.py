from celery.decorators import task
from celery.utils.log import get_task_logger

from .email_helper import send_signup_confirmation

logger = get_task_logger(__name__)


@task(name="send_signup_email_task")
def send_signup_email_task(user):
    """sends an email when signup form is filled successfully"""
    logger.info("Sent signup email")
    return send_signup_confirmation(user)
