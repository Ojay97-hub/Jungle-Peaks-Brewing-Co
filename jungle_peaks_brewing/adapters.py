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
        Override to check if this is a social account signup.
        Social accounts should not require email verification.
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
        Don't send confirmation email for social account signups
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
        Allow automatic signup for social accounts without email verification.
        """
        return True
    
    def save_user(self, request, sociallogin, form=None):
        """
        Save the user and mark their email as verified since it's from a trusted provider.
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

