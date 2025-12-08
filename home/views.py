import json

from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages

from .forms import NewsletterForm
from .models import NewsletterSubscriber
from products.models import Product


def index(request):
    """
    Render the homepage.

    Template Used:
    - home/home.html
    """
    # Get the featured beer (Citrus Peak IPA)
    featured_beer = None
    try:
        featured_beer = Product.objects.get(name="Citrus Peak IPA")
    except Product.DoesNotExist:
        pass
    
    context = {
        'featured_beer': featured_beer,
    }
    return render(request, 'home/home.html', context)



@csrf_exempt
def newsletter_signup(request):
    """
    Handle newsletter signup.

    Models Used:
    - NewsletterSubscriber: Stores email subscribers.

    Request Type:
    - POST: Expects JSON data with an "email" field.

    Response:
    - JSON response indicating success or failure.
    - If successful, returns the newly created subscriber's ID.
    - If the email already exists, returns an error message.

    Example JSON Request:
    ```json
    {
        "email": "user@example.com"
    }
    ```

    Example JSON Response:
    ```json
    {
        "success": True,
        "subscriber_id": 123
    }
    ```
    """
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            email = data.get("email")

            if NewsletterSubscriber.objects.filter(email=email).exists():
                return JsonResponse({
                    "success": False,
                    "message": "Email already subscribed."
                })

            # Create a new subscriber without interests (interests added later)
            subscriber = NewsletterSubscriber.objects.create(email=email)

            return JsonResponse({
                "success": True,
                "subscriber_id": subscriber.id
            })

        except json.JSONDecodeError:
            return JsonResponse({
                "success": False,
                "message": "Invalid JSON format."
            })

    return JsonResponse({
        "success": False,
        "message": "Invalid request method."
    })


@csrf_exempt
def set_interests(request):
    """
    Save user interests after newsletter signup.

    Models Used:
    - NewsletterSubscriber: Updates subscriber's interests.

    Request Type:
    - POST: Expects JSON data with `subscriber_id` and a list of interests.

    Response:
    - JSON response indicating success or failure.
    - If the subscriber ID is invalid, returns an error message.

    Example JSON Request:
    ```json
    {
        "subscriber_id": 123,
        "interests": ["craft beer", "brewery events"]
    }
    ```

    Example JSON Response:
    ```json
    {
        "success": True
    }
    ```
    """
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            subscriber_id = data.get("subscriber_id")
            selected_interests = data.get("interests", [])

            # Ensure subscriber_id is provided
            if not subscriber_id:
                return JsonResponse({
                    "success": False,
                    "message": "Missing subscriber ID."
                })

            subscriber = NewsletterSubscriber.objects.get(id=subscriber_id)

            # Ensure at least one interest is selected
            if not selected_interests:
                return JsonResponse({
                    "success": False,
                    "message": "No interests selected."
                })

            subscriber.interests = ",".join(selected_interests)
            subscriber.save()

            return JsonResponse({"success": True})

        except NewsletterSubscriber.DoesNotExist:
            return JsonResponse({
                "success": False,
                "message": "Subscriber not found."
            })

        except json.JSONDecodeError:
            return JsonResponse({
                "success": False,
                "message": "Invalid JSON format."
            })

    return JsonResponse({
        "success": False,
        "message": "Invalid request method."
    })