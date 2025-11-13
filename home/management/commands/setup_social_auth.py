"""
Management command to set up Google OAuth authentication
"""
import os
from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialApp


class Command(BaseCommand):
    help = 'Set up Google OAuth authentication from environment variables'

    def handle(self, *args, **options):
        # Get or create the default site
        """
        Configure or update the Google OAuth SocialApp from environment variables and attach it to the current Site.
        
        Reads GOOGLE_OAUTH_CLIENT_ID and GOOGLE_OAUTH_CLIENT_SECRET from the environment, validates them, creates or updates the `SocialApp` with provider 'google' using those credentials, associates the app with the current Site, and writes progress, success, and next-step messages to stdout.
        """
        site = Site.objects.get_current()
        self.stdout.write(f'Using site: {site.name} ({site.domain})')

        # Google OAuth Setup
        google_client_id = os.environ.get('GOOGLE_OAUTH_CLIENT_ID')
        google_client_secret = os.environ.get('GOOGLE_OAUTH_CLIENT_SECRET')

        if not google_client_id or not google_client_secret:
            self.stdout.write(self.style.ERROR('[ERROR] Google OAuth credentials not found in environment'))
            self.stdout.write('  Make sure GOOGLE_OAUTH_CLIENT_ID and GOOGLE_OAUTH_CLIENT_SECRET are set in env.py')
            return

        if google_client_secret == 'YOUR_GOOGLE_CLIENT_SECRET_HERE':
            self.stdout.write(self.style.ERROR('[ERROR] Google Client Secret is still a placeholder'))
            self.stdout.write('  Replace YOUR_GOOGLE_CLIENT_SECRET_HERE with your actual secret in env.py')
            return

        # Create or update Google OAuth app
        google_app, created = SocialApp.objects.update_or_create(
            provider='google',
            defaults={
                'name': 'Google OAuth',
                'client_id': google_client_id,
                'secret': google_client_secret,
            }
        )
        google_app.sites.add(site)
        
        if created:
            self.stdout.write(self.style.SUCCESS('[SUCCESS] Google OAuth configured successfully!'))
        else:
            self.stdout.write(self.style.SUCCESS('[SUCCESS] Google OAuth updated successfully!'))

        self.stdout.write('\n' + self.style.SUCCESS('Setup complete!'))
        self.stdout.write('\nNext steps:')
        self.stdout.write('1. Make sure redirect URI is configured in Google Cloud Console:')
        self.stdout.write('   -> http://127.0.0.1:8000/accounts/google/login/callback/')
        self.stdout.write('2. Start your server: python manage.py runserver')
        self.stdout.write('3. Visit: http://127.0.0.1:8000/accounts/signup/')
        self.stdout.write('4. You should see "Sign up with Google" button!')
        self.stdout.write('\n' + self.style.WARNING('Note: Make sure you added the redirect URI in Google Cloud Console first!'))
