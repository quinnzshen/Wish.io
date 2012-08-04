from django.http import HttpResponse

def home(request):
    return HttpResponse("You're at the home page!")

def register(request):
    return HttpResponse("You're at the register page!")

def mywishlist(request):
    return HttpResponse("You're at mywishlist!")
