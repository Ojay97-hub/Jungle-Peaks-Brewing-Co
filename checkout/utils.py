"""Utility helpers for the checkout application."""

import logging
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.template.loader import render_to_string

logger = logging.getLogger(__name__)


def _get_sendgrid_client():
    """Return SendGrid client or raise if not configured."""
    api_key = os.getenv('SENDGRID_API_KEY')
    if not api_key:
        raise ImproperlyConfigured(
            "SENDGRID_API_KEY environment variable is required for email sending."
        )
    return SendGridAPIClient(api_key)


def should_use_sendgrid():
    """Check if we should use SendGrid API for email sending."""
    return bool(os.getenv('SENDGRID_API_KEY') and os.getenv('DEFAULT_FROM_EMAIL'))


def _get_from_email():
    """Return the configured sender address or raise if missing."""
    from_email = getattr(settings, "DEFAULT_FROM_EMAIL", None)
    if not from_email:
        raise ImproperlyConfigured(
            "DEFAULT_FROM_EMAIL must be configured to send emails."
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

    # Check if we should use SendGrid API
    if should_use_sendgrid():
        print(f"📧 Using SendGrid API for order {order.order_number}")

        # Create SendGrid email
        from_email = Email(_get_from_email())
        to_email = To(order.email)
        content = Content("text/plain", body)

        mail = Mail(from_email, to_email, subject, content)

        try:
            sg = _get_sendgrid_client()
            response = sg.send(mail)

            # Log success with details
            logger.info("Confirmation email dispatched for order %s - Status: %s", order.order_number, response.status_code)

            # SendGrid success status codes
            if response.status_code in [200, 201, 202]:
                print(f"✅ Email sent successfully for order {order.order_number} - Status: {response.status_code}")
                return 1
            else:
                # Log non-success status codes
                logger.warning("Email sent but with non-success status for order %s: %s - %s",
                             order.order_number, response.status_code, response.body)
                print(f"⚠️ Email sent with status {response.status_code} for order {order.order_number}")
                return 0

        except Exception as e:
            # Enhanced error logging with more details
            error_msg = str(e)
            logger.error("Failed to send confirmation email for order %s: %s", order.order_number, error_msg)

            # Print error for immediate debugging
            print(f"❌ Failed to send email for order {order.order_number}: {error_msg}")

            # Additional debugging info
            if hasattr(e, 'status_code'):
                print(f"   HTTP Status Code: {e.status_code}")
            if hasattr(e, 'body'):
                print(f"   Response Body: {e.body}")

            return 0
    else:
        # Fall back to Django's email backend (console in development)
        print(f"📧 Using Django email backend for order {order.order_number}")

        from django.core.mail import send_mail
        try:
            sent = send_mail(subject, body, _get_from_email(), [order.email])
            logger.info("Confirmation email dispatched for order %s via Django backend", order.order_number)
            print(f"✅ Email sent successfully for order {order.order_number} via Django backend")
            return sent
        except Exception as e:
            logger.error("Failed to send confirmation email for order %s via Django backend: %s", order.order_number, str(e))
            print(f"❌ Failed to send email for order {order.order_number} via Django backend: {str(e)}")
            return 0


def test_sendgrid_configuration():
    """Test function to verify SendGrid configuration is working."""
    try:
        print("🔧 Testing SendGrid Configuration...")

        # Test 1: Check if we should use SendGrid
        if not should_use_sendgrid():
            print("❌ SendGrid not configured - missing API key or from email")
            return False

        print("✅ SendGrid configuration detected")

        # Test 2: Check if from email is configured
        from_email = _get_from_email()
        print(f"✅ DEFAULT_FROM_EMAIL: {from_email}")

        # Test 3: Try to create SendGrid client
        sg = _get_sendgrid_client()
        print("✅ SendGrid client created successfully")

        # Test 4: Try to send a test email
        test_email = Mail(
            Email(from_email),
            To("owencotter97@gmail.com"),
            "SendGrid Configuration Test",
            Content("text/plain", "This is a test email to verify SendGrid configuration.")
        )

        response = sg.send(test_email)
        if response.status_code in [200, 201, 202]:
            print(f"✅ Test email sent successfully - Status: {response.status_code}")
            return True
        else:
            print(f"⚠️ Test email sent but with status: {response.status_code}")
            if hasattr(response, 'body'):
                print(f"   Response Body: {response.body}")
            return False

    except Exception as e:
        print(f"❌ SendGrid configuration test failed: {str(e)}")
        if hasattr(e, 'status_code'):
            print(f"   HTTP Status Code: {e.status_code}")
        if hasattr(e, 'body'):
            print(f"   Response Body: {e.body}")
        return False
