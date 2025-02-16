import json
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from .forms import NewsletterForm
from .models import NewsletterSubscriber

# Create your views here.
def index(request):
    """ A view to return the home page """
    return render(request, 'home/home.html')

# newsletter_signup and set_interests functions
@csrf_exempt
def newsletter_signup(request):
    """Handles newsletter signup with interest selection"""
    if request.method == "POST":
        data = json.loads(request.body)
        email = data.get("email")

        if NewsletterSubscriber.objects.filter(email=email).exists():
            return JsonResponse({"success": False, "message": "Email already subscribed."})

        # Create a temporary subscriber (interests added later)
        subscriber = NewsletterSubscriber.objects.create(email=email)

        return JsonResponse({"success": True, "subscriber_id": subscriber.id})

    return JsonResponse({"success": False, "message": "Invalid request."})


@csrf_exempt
def set_interests(request):
    """Handles saving user interests after signup"""
    if request.method == "POST":
        data = json.loads(request.body)
        subscriber_id = data.get("subscriber_id")
        selected_interests = data.get("interests", [])

        try:
            subscriber = NewsletterSubscriber.objects.get(id=subscriber_id)
            subscriber.interests = ",".join(selected_interests)  # Convert list to CSV string
            subscriber.save()
            return JsonResponse({"success": True})
        except NewsletterSubscriber.DoesNotExist:
            return JsonResponse({"success": False, "message": "Subscriber not found."})

    return JsonResponse({"success": False, "message": "Invalid request."})