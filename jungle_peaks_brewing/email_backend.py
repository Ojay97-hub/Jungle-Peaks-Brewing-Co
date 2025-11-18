"""Custom Django email backend using SendGrid API."""

import logging
from django.core.mail.backends.base import BaseEmailBackend
from django.core.mail import EmailMessage
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content
import os

logger = logging.getLogger(__name__)


class SendGridEmailBackend(BaseEmailBackend):
    """Custom Django email backend that uses SendGrid API."""

    def __init__(self, fail_silently=False, **kwargs):
        super().__init__(fail_silently=fail_silently)
        self.api_key = os.getenv('SENDGRID_API_KEY')
        if not self.api_key:
            if fail_silently:
                logger.warning("SENDGRID_API_KEY not set - emails will not be sent")
            else:
                raise ValueError("SENDGRID_API_KEY environment variable is required")

    def send_messages(self, email_messages):
        """Send email messages using SendGrid API."""
        if not email_messages:
            return 0

        if not self.api_key:
            logger.error("SENDGRID_API_KEY not set - cannot send emails")
            if not self.fail_silently:
                raise ValueError("SENDGRID_API_KEY environment variable is required")
            return 0

        sent_count = 0

        for email in email_messages:
            try:
                # Convert Django EmailMessage to SendGrid format
                mail = self._django_to_sendgrid(email)
                if not mail:
                    logger.warning("Failed to convert email to SendGrid format - skipping")
                    continue
                
                sg = SendGridAPIClient(self.api_key)
                response = sg.send(mail)

                if response.status_code in [200, 201, 202]:
                    sent_count += 1
                    logger.info(
                        f"Email sent successfully via SendGrid API - "
                        f"To: {email.to}, Subject: {email.subject}, Status: {response.status_code}"
                    )
                else:
                    error_msg = f"Email failed to send - Status: {response.status_code}"
                    if hasattr(response, 'body'):
                        error_msg += f", Body: {response.body}"
                    logger.error(error_msg)
                    if not self.fail_silently:
                        raise Exception(error_msg)

            except Exception as e:
                error_msg = f"Failed to send email via SendGrid API: {str(e)}"
                logger.error(error_msg)
                if not self.fail_silently:
                    raise Exception(error_msg)

        return sent_count

    def _django_to_sendgrid(self, email):
        """Convert Django EmailMessage to SendGrid Mail object."""
        try:
            # Handle from email
            from_email = email.from_email or self._get_default_from_email()
            if isinstance(from_email, str):
                from_email = Email(from_email)

            # Handle recipients (Django EmailMessage.to is a list)
            to_emails = []
            if hasattr(email, 'to') and email.to:
                for recipient in email.to:
                    if isinstance(recipient, str):
                        to_emails.append(To(recipient))

            if not to_emails:
                return None

            # Create subject and content
            subject = email.subject or ""

            # Handle content - check for HTML alternative first
            content = None
            if hasattr(email, 'alternatives') and email.alternatives:
                for alt_content, alt_type in email.alternatives:
                    if alt_type == 'text/html' and alt_content:
                        content = Content("text/html", alt_content)
                        break

            # Fall back to plain text body
            if not content:
                body_content = email.body if hasattr(email, 'body') else ""
                content = Content("text/plain", body_content or "")

            # Create SendGrid mail object
            mail = Mail(from_email, to_emails, subject, content)

            # Add reply-to if present
            if hasattr(email, 'reply_to') and email.reply_to:
                reply_to_list = email.reply_to if isinstance(email.reply_to, (list, tuple)) else [email.reply_to]
                if reply_to_list and reply_to_list[0]:
                    mail.reply_to = Email(str(reply_to_list[0]))

            return mail

        except Exception as e:
            logger.error(f"Error converting Django email to SendGrid format: {str(e)}")
            return None

    def _get_default_from_email(self):
        """Get default from email address."""
        from django.conf import settings
        return getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@example.com')
