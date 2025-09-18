"""Utility helpers for the checkout application."""

import logging

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.mail import send_mail
from django.template.loader import render_to_string

logger = logging.getLogger(__name__)


def _get_from_email():
    """Return the configured sender address or raise if missing."""
    from_email = getattr(settings, "DEFAULT_FROM_EMAIL", None) or getattr(
        settings, "EMAIL_HOST_USER", None
    )
    if not from_email:
        raise ImproperlyConfigured(
            "DEFAULT_FROM_EMAIL or EMAIL_HOST_USER must be configured to send emails."
        )
    return from_email


def send_order_confirmation_email(order):
    """Send the standard confirmation email for the supplied order."""
    context = {"order": order, "contact_email": _get_from_email()}
    subject = render_to_string(
        "checkout/confirmation_emails/confirmation_email_subject.txt", context
    ).strip()
    body = render_to_string(
        "checkout/confirmation_emails/confirmation_email_body.txt", context
    )

    recipients = [order.email]
    sent = send_mail(subject, body, context["contact_email"], recipients)
    logger.info("Confirmation email dispatched for order %s", order.order_number)
    return sent
