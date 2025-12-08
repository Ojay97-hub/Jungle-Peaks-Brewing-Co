"""Utility helpers for the checkout application."""

import logging
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.mail import send_mail
from django.template.loader import render_to_string

logger = logging.getLogger(__name__)


def _get_from_email():
    """Return the configured sender address or raise if missing."""
    from_email = getattr(settings, "DEFAULT_FROM_EMAIL", None)
    if not from_email:
        raise ImproperlyConfigured(
            "DEFAULT_FROM_EMAIL must be configured to send emails."
        )
    return from_email


def send_order_confirmation_email(order):
    """Send the standard confirmation email for the supplied order.
    
    Uses Django's standard email backend (configured in settings.py).
    Returns 1 on success, 0 on failure.
    """
    context = {"order": order, "contact_email": _get_from_email()}
    subject = render_to_string(
        "checkout/confirmation_emails/confirmation_email_subject.txt", context
    ).strip()
    body = render_to_string(
        "checkout/confirmation_emails/confirmation_email_body.txt", context
    )

    try:
        sent = send_mail(
            subject=subject,
            message=body,
            from_email=_get_from_email(),
            recipient_list=[order.email],
            fail_silently=False
        )
        logger.info(
            "Confirmation email dispatched for order %s", 
            order.order_number
        )
        print(f"✅ Email sent successfully for order {order.order_number}")
        return sent
    except Exception as e:
        logger.error(
            "Failed to send confirmation email for order %s: %s", 
            order.order_number, 
            str(e)
        )
        print(f"❌ Failed to send email for order {order.order_number}: {str(e)}")
        return 0
