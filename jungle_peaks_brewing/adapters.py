"""
Custom adapters for django-allauth to handle redirects, social linking, and verification.
"""
from django.conf import settings
from django.shortcuts import resolve_url
from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.utils import user_email, user_username
import logging

logger = logging.getLogger(__name__)

class CustomAccountAdapter(DefaultAccountAdapter):
    """
    Custom account adapter to handle redirects and verification logic smoothly.
    """
    
    def get_login_redirect_url(self, request):
        """
        Ensure the 'next' parameter is respected after login.
        """
        # Check for 'next' parameter in POST or GET
        next_url = request.POST.get('next') or request.GET.get('next')
        
        # If next_url exists and is safe, return it
        if next_url and self.is_safe_url(next_url):
            return next_url
            
        # Fallback to default behavior (settings.LOGIN_REDIRECT_URL)
        return resolve_url(settings.LOGIN_REDIRECT_URL)

    def get_signup_redirect_url(self, request):
        """
        Ensure the 'next' parameter is respected after signup.
        """
        # Check for 'next' parameter in POST or GET
        next_url = request.POST.get('next') or request.GET.get('next')
        
        # If next_url exists and is safe, return it
        if next_url and self.is_safe_url(next_url):
            return next_url
            
        # Fallback to default behavior
        return resolve_url(settings.LOGIN_REDIRECT_URL)

    def is_email_verification_mandatory(self, request):
        """
        Make email verification optional to avoid blocking checkout.
        Settings: ACCOUNT_EMAIL_VERIFICATION = 'optional' handles the enforcement,
        but we ensure here we don't force it.
        """
        return False


class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    """
    Custom social account adapter to handle account linking and redirects.
    """

    def is_auto_signup_allowed(self, request, sociallogin):
        # Allow auto signup
        return True

    def pre_social_login(self, request, sociallogin):
        """
        Invoked just after a user successfully authenticates via a social provider,
        but before the login is actually processed.
        
        We rely on SOCIALACCOUNT_EMAIL_AUTHENTICATION_AUTO_CONNECT = True in settings
        to handle automatic linking of social accounts to existing users with the same email.
        
        However, we can add custom logic here if needed.
        """
        # Ensure the email is marked as verified if it comes from a trusted provider
        # This prevents allauth from asking to verify an email that Google already verified
        if sociallogin.account.provider == 'google':
            if sociallogin.email_addresses:
                for email in sociallogin.email_addresses:
                    email.verified = True
        
        return super().pre_social_login(request, sociallogin)

    def get_connect_redirect_url(self, request, socialaccount):
        """
        URL to redirect to after successfully connecting a social account.
        """
        next_url = request.POST.get('next') or request.GET.get('next')
        if next_url:
            return next_url
        return super().get_connect_redirect_url(request, socialaccount)
