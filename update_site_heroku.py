#!/usr/bin/env python
"""Script to update Site domain to match Heroku domain"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jungle_peaks_brewing.settings')
django.setup()

from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialApp

# Check current site
site = Site.objects.get_current()
print(f"Current Site: {site.domain} ({site.name})")

# Update to Heroku domain
site.domain = 'jungle-peaks-update.herokuapp.com'
site.name = 'Jungle Peaks'
site.save()
print(f"Updated Site: {site.domain}")

# Check SocialApp
apps = SocialApp.objects.all()
print(f"\nSocialApps count: {apps.count()}")
for app in apps:
    print(f"  - {app.provider}: {app.name}")
    print(f"    Client ID: {app.client_id}")
    print(f"    Sites: {list(app.sites.all())}")

