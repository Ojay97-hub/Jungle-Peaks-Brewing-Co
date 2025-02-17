from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages


# Create your views here.
def contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        # Send email (replace with actual settings)
        send_mail(
            subject=f"New Contact Form Submission from {name}",
            message=f"Message from {name} ({email}):\n\n{message}",
            from_email="your_email@example.com",
            recipient_list=["info@junglepeaksbrew.com"],
            fail_silently=False,
        )

        messages.success(request, "🎉 Your message has been sent successfully!")
        return redirect("contact")  # Redirect to the same page

    return render(request, "contact.html")