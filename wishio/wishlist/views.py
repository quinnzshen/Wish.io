from django.template import Context
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from wishlist.models import User, Item, WishList
from urllib2 import urlopen
from django.core.exceptions import ObjectDoesNotExist
from scraper import amazonread, ebayread, targetread, macysread, bbuyread
# from PIL import Image, ImageOps
import urllib
import os
from django.conf import settings

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


def create_resized_image(image_name, original_location, xconstrain=250, yconstrain=250):
    """
    Takes an input URL for an image, a name for the image for it to be saved as, 
    and the optional xconstrain and yconstrain options, which are used to define the
    constraints to resize the image to. If these are not specified, they will default
    to 200px each. Returns the path to the image
    """

    if not os.path.exists('%s/images/resized/%s.jpg' % (settings.MEDIA_ROOT, image_name)): # Ensure a resized image doesn't already exist in the default MEDIA_ROOT/images/resized (MEDIA_ROOT is defined in Django's settings)
        unsized_image = urllib.urlretrieve(str(original_location)) # Fetch original image
        unsized_image = Image.open(unsized_image[0]) # Load the fetched image
        resized_image = ImageOps.fit(unsized_image, (xconstrain, yconstrain), Image.ANTIALIAS) # Create a resized image by fitting the original image into the constrains, and do this using proper antialiasing
        resized_image = resized_image.convert("RGB") # PIL sometimes throws errors if this isn't done
        resized_image.save('%s/images/resized/%s.jpg' % (settings.MEDIA_ROOT, image_name), 'jpeg') # Save the resized image as a jpeg into the MEDIA_ROOT/images/resized
        
    return '%s/images/resized/%s.jpg' % (settings.MEDIA_ROOT, image_name)

def wishlist(request, board_id = '1'):
    # if 'user' not in request.session:
    #     return HttpResponseRedirect('/')

    user = request.session['user']
    wishlist = WishList.objects.get(pk=board_id)

    def add_item(url):
        if "amazon" in url:
            result = amazonread(url)
            # photo = create_resized_image(result['title'], result['image'])
            name = result['title']
            item = Item(name=name, url=url, price=10000, photo=result['image'])
            item.wishlist = wishlist
            item.save()
        elif "ebay" in url:
            result = ebayread(url)
            # photo = create_resized_image(result['title'], result['image'])
            name = result['title']
            item = Item(name=name, url=url, price=10000, photo=result['image'])
            item.wishlist = wishlist
            item.save()
        elif "bestbuy" in url:
            result = bbuyread(url)
            # photo = create_resized_image(result['title'], result['image'])
            name = result['title']
            item = Item(name=name, url=url, price=10000, photo=result['image'])
            item.wishlist = wishlist
            item.save()
        elif "target" in url:
            result = targetread(url)
            # photo = create_resized_image(result['title'], result['image'])
            name = result['title']
            item = Item(name=name, url=url, price=10000, photo=result['image'])
            item.wishlist = wishlist
            item.save()
        elif "macys" in url:
            result = macysread(url)
            # photo = create_resized_image(result['title'], result['image'])
            name = result['title']
            item = Item(name=name, url=url, price=10000, photo=result['image'])
            item.wishlist = wishlist
            item.save()

    if request.method == "POST":
        url = request.POST['url']
        add_item(url)
        return HttpResponseRedirect('/wishlist/' + str(user.wishlist.pk))



    items = [item for item in Item.objects.filter(wishlist=wishlist)]
    
    con = Context({
            'wishlist': wishlist,
            'items': items,
        })
    con.update(csrf(request))
    return render_to_response('wishlist.html', con)


def friends(request):
    return HttpResponse("You're at the friend page!")
