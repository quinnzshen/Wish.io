from django.template import Context
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from wishlist.models import User, Item, WishList
from urllib2 import urlopen
from django.core.exceptions import ObjectDoesNotExist

def home(request):
    if request.method == 'POST':
        try: 
            user = User.objects.get(name=request.POST['user'])
            if user.password == request.POST['password']:
                request.session['user'] = user
                url = '/wishlist/' + str(user.wishlist.pk)
                return HttpResponseRedirect(url)
        except:
            return HttpResponseRedirect('/register/')

    con = Context()
    con.update(csrf(request))
    return render_to_response('index.html', con)

def register(request):
    con = Context()

    if "register" in request.POST:
        # Try clause checks if all fields are filled out.
        try:
            username = request.POST['user']
            password = request.POST['password']
        except ObjectDoesNotExist:
            con['empty_fields'] = True
            con.update(crsf(request))
            return render_to_response('register.html', con)

        new_user = User.objects.create(
            name=username,
            password=password
        )

        # Creates a default public wishlist for the new user
        wishlist_name = username  + "'s Wishlist"
        new_user.wishlist = WishList.objects.create(
            name=wishlist_name,
            privacy='public',
            owner=new_user,
        )

        new_user.save()

        request.method = None

        # Redirects user to the log in page.
        return HttpResponseRedirect('/')

    con.update(csrf(request))
    return render_to_response('register.html', con)


def wishlist(request, board_id = '1'):
    # if 'user' not in request.session:
    #     return HttpResponseRedirect('/')

    wishlist = WishList.objects.get(pk=board_id)

    def add_item(url):
        response = urlopen(url)
        html = response.read()
        #script to retrieve
        item = Item(name="Dress", url=url, price=1000.00)
        item.wishlist = wishlist
        item.save()

    add_item("http://www.google.com")
    add_item("http://www.google.com")
    add_item("http://www.google.com")
    add_item("http://www.google.com")

    items = [item for item in Item.objects.filter(wishlist=wishlist)]
    
    con = Context({
            'wishlist': wishlist,
        })
    return render_to_response('wishlist.html', con)


def friends(request):
    return HttpResponse("You're at the friend page!")
