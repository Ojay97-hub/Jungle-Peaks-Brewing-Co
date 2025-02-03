from django.shortcuts import render 

# Create your views here.
def tours(request):
    # your logic here
    return render(request, 'tours/tours.html')
