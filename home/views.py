from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from .forms import NewsletterForm
from .models import NewsletterSubscriber

# Create your views here.
def index(request):
    """ A view to return the home page """
    return render(request, 'home/home.html')

# newsletter_signup view
def newsletter_signup(request):
    if request.method == "POST":
        form = NewsletterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]

            # Check if email already exists
            if NewsletterSubscriber.objects.filter(email=email).exists():
                messages.warning(request, "You're already subscribed!")
            else:
                form.save()
                messages.success(request, "Thank you for subscribing!")
            
              # Redirect properly to ensure messages persist
            return HttpResponseRedirect(reverse("home"))

    return redirect("home")  # Redirect back if accessed directly