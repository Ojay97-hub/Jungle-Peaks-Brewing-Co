"""
Custom account views for django-allauth email verification
"""
from django.shortcuts import redirect
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_protect
from allauth.account.models import EmailAddress
from allauth.account.utils import send_email_confirmation
import logging

logger = logging.getLogger(__name__)


@require_http_methods(["GET", "POST"])
@csrf_protect
def resend_verification_email(request):
    """
    Resend verification email for unauthenticated users.
    Works with email address from POST data or session.
    """
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        
        if not email:
            # Try to get email from session (stored during signup)
            email = request.session.get('account_verified_email', '')
        
        if not email:
            messages.error(request, "Please provide your email address.")
            return redirect('account_email_verification_sent')
        
        try:
            # Find the email address
            email_address = EmailAddress.objects.get(email__iexact=email)
            
            # Check if already verified
            if email_address.verified:
                messages.info(request, f"The email address {email} is already verified.")
                return redirect('account_login')
            
            # Get the user from the email address
            user = email_address.user
            
            # Send confirmation email - send_email_confirmation expects (request, user, email, signup)
            send_email_confirmation(request, user, email=email, signup=False)
            messages.success(
                request,
                f"A verification email has been sent to {email}. Please check your inbox."
            )
            logger.info(f"Verification email resent to {email}")
            
        except EmailAddress.DoesNotExist:
            messages.error(
                request,
                f"No account found with email address {email}. Please check your email and try again."
            )
            logger.warning(f"Attempted to resend verification for non-existent email: {email}")
        except Exception as e:
            logger.error(f"Failed to resend verification email to {email}: {str(e)}", exc_info=True)
            messages.error(
                request,
                "We couldn't send the verification email right now. Please try again later."
            )
    
    # Redirect back to verification sent page
    return redirect('account_email_verification_sent')

