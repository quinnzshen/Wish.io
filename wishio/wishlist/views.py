from django.http import HttpResponse
from wishlist.models import

def home(request):
    return HttpResponse("You're at the home page!")

def register(request):
    return HttpResponse("You're at the register page!")

def wishlist(request, board_id = '1'):
    return HttpResponse("You're at uid = %s" % board_id)

def friends(request):
    return HttpResponse("You're at the friend page!")
