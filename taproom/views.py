from django.shortcuts import render 

# Create your views here.
def taproom(request):
    return render(request, 'taproom/taproom.html')