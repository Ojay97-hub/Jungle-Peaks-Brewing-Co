from django.shortcuts import render, redirect
from django.contrib import messages

from .forms import ContactForm


def contact_view(request):
    """
    Handle contact form submissions.

    Models Used:
    - ContactForm: Handles user-submitted contact messages.

    Request Type:
    - GET: Displays the contact form.
    - POST: Processes and saves the contact form data.

    Response:
    - If valid, saves the form and displays a success message.
    - If invalid, reloads the form with errors.

    Template Used:
    - contact.html

    Redirects:
    - contact: After successful form submission.

    Example Success Message:
    ✅ Your message has been sent successfully!
    """
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Your message has been sent successfully!")
            return redirect('contact:contact')
    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form})
