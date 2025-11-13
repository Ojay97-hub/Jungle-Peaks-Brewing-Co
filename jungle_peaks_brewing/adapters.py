"""
Custom adapters for django-allauth
"""
from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter


class CustomAccountAdapter(DefaultAccountAdapter):
    """
    Custom account adapter to handle email verification differently for social accounts
    """
    
    def is_email_verification_mandatory(self, request):
        """
        Determine whether email verification is required for the incoming request.
        
        Returns `False` for social signups detected by a session sociallogin entry or known social provider callback paths (e.g., Google, Facebook); otherwise defers to the default behavior.
        
        Returns:
            `True` if email verification should be required, `False` otherwise.
        """
        # Check if user is authenticating via social account
        # Look for social login in session or URL path
        if hasattr(request, 'session'):
            if request.session.get('socialaccount_sociallogin'):
                return False
        
        # Check if this is a social callback URL
        if hasattr(request, 'path'):
            if '/accounts/google/' in request.path or '/accounts/facebook/' in request.path:
                return False
        
        # For regular signups, use the default behavior
        return super().is_email_verification_mandatory(request)
    
    def send_confirmation_mail(self, request, emailconfirmation, signup):
        """
        Skip sending confirmation emails for social-account signups.
        
        If the email address is associated with a user who has one or more social accounts,
        mark that EmailAddress as verified and do not send a confirmation email. For all
        other signups, delegate to the superclass implementation to send the confirmation.
        
        Parameters:
            request: The current Django HttpRequest.
            emailconfirmation: allauth EmailConfirmation instance for the target email address.
            signup: Boolean-like flag indicating whether this is part of a signup flow.
        """
        # Check if user has social accounts
        if hasattr(emailconfirmation.email_address, 'user') and emailconfirmation.email_address.user:
            user = emailconfirmation.email_address.user
            if user.socialaccount_set.exists():
                # User signed up via social auth, don't send verification email
                # Mark as verified immediately
                emailconfirmation.email_address.verified = True
                emailconfirmation.email_address.save()
                return
        
        # For regular email signups, send the email
        super().send_confirmation_mail(request, emailconfirmation, signup)


class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    """
    Custom adapter to automatically verify emails from social providers
    """
    
    def is_auto_signup_allowed(self, request, sociallogin):
        """
        Allow automatic creation of a user account for incoming social logins.
        
        @returns
            True to permit automatic signup for the given social login, `False` to require explicit signup.
        """
        return True
    
    def save_user(self, request, sociallogin, form=None):
        """
        Save a user created from a social login and ensure any emails provided by the social provider are marked verified.
        
        If the social login includes email addresses, those addresses are created or updated on the saved user with `verified = True` and `primary = True` so they do not require further verification.
        
        Returns:
            The saved User model instance.
        """
        user = super().save_user(request, sociallogin, form)
        
        # Mark the email as verified immediately
        if sociallogin.email_addresses:
            from allauth.account.models import EmailAddress
            for email_address in sociallogin.email_addresses:
                email_obj, created = EmailAddress.objects.get_or_create(
                    user=user,
                    email=email_address.email.lower(),
                    defaults={'verified': True, 'primary': True}
                )
                if not created and not email_obj.verified:
                    email_obj.verified = True
                    email_obj.primary = True
                    email_obj.save()
        
        return user
