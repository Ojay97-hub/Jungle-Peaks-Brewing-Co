from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ContactForm

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Your message has been sent successfully!")
            return redirect('contact:contact')   # Redirect back to the same page
    else:
        form = ContactForm()
    
    return render(request, 'contact.html', {'form': form})