# boosts/tasks.py

import os

from celery import shared_task
from celery.utils.log import get_task_logger
from django.conf import settings
from django.core.mail import send_mail

from .models import Inspirational

if settings.ENVIRONMENT == "development":
    from dotenv import load_dotenv

    load_dotenv()

TEST_EMAIL_ADDRESS = os.getenv("TEST_EMAIL_ADDRESS")

logger = get_task_logger(__name__)


@shared_task
def send_inspirational_to_beastie(
    user_username,
    user_email,
    user_beastie_email,
    user_beastie_username,
    message,
):
    """
    Sends the `Inspirational` to User's `Beastie` and CC to User's own email.
    """
    logger.info("\nLOGGER: Sending inspirational quote to beastie.")
    # Send the inspirational quote to the user's beastie:
    send_mail(
        f"Inspirational Quote from your Beastie: {user_username}",
        message,
        user_email,
        [user_beastie_email],
        fail_silently=False,
    )
    logger.info("LOGGER: Sent inspirational quote to beastie.")
    logger.info("LOGGER: Sending inspirational quote cc to user.")
    # Send a copy of the inspirational quote to the user:
    send_mail(
        f"You Sent an Inspirational Quote to your Beastie: {user_beastie_username}",
        message,
        user_email,
        [user_email],
        fail_silently=False,
    )
    logger.info("LOGGER: Sent inspirational quote cc to user.")


@shared_task
def send_inspirational_to_self(user_id, inspirational_id=None):
    """
    If inspirational_id is given, use that; otherwise fall back to the first
    Inspirational for the user.
    """
    # start with all that belong to the user
    qs = Inspirational.objects.filter(author_id=user_id)
    # if a specific one was passed in, narrow down to it
    if inspirational_id is not None:
        qs = qs.filter(pk=inspirational_id)
    inspirational = qs.first()
    if not inspirational:
        # nothing to send
        return

    # send the daily inspiration
    send_mail(
        subject="Your Daily Inspiration",
        message=inspirational.body,
        from_email=inspirational.author.email,
        recipient_list=[inspirational.author.email],
        fail_silently=False,
    )


@shared_task
def send_test_email():
    """
    Sends a test email to the admin.
    """
    send_mail(
        subject="Test Email from Boosts",
        message="This is the test email body.",
        from_email=TEST_EMAIL_ADDRESS,
        recipient_list=[TEST_EMAIL_ADDRESS],
    )
    logger.info("Sent test email.")


@shared_task
def log_to_console():
    logger.info("LOGGER: This is a test.")
