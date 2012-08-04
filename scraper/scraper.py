#!/usr/bin/env python

''' 
#A script that parses the html content of a url to get: 
    title, 
    price, 
    website (it really gets url base, eg www.amazon.com -> amazon), 
    image 
#Puts it all nto a python dictionary with the same keywords
#Now supports amazon, ebay, bestbuy, target, macy's
#Author: Timur Bazhirov - bazhirov.com
'''

print "Usage: change/uncomment the desired url in the source and run"

import os
import sys
import types
import urllib
import urllib2
import re
from BeautifulSoup import BeautifulSoup

NO_IMAGE_URL = "https://encrypted-tbn1.google.com/images?q=tbn:ANd9GcSHSGrRjaWRTAlaHGrv-8TSwk8D17qmYFc1xfZiV2r8BTD_jG\
mhLA"

#amazon parser - gets the title, price and website name

def amazonread(string):

    print "In AmazonRead: ", string.encode('utf-8')

    article = string.encode('utf-8')

    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]

    try:
        resource = opener.open(article)
    except TypeError:
        print "Oops! Url is broken", article
        return "No info available now"
        pass
    data = resource.read()
    resource.close()

    soup = BeautifulSoup(data)

    try:
        price = soup.find(['b','span'],attrs={"class":"priceLarge"})
    except TypeError:
        try: 
            price = soup.find(['b','span'],attrs={"class":"priceLarge kitsunePrice"})
        except TypeError:
            price = "N/A"
            pass
        if price != "N/A":
           price = price.renderContents()
        pass

    try:
        title = soup.find('span',id="btAsinTitle")
    except TypeError:
        try:
            title = soup.find('h1',attrs={"class":"parseasinTitle"})
        except TypeError:
            title = "N/A"
        if title != "N/A":
            title = title.renderContents()
        pass

    try:
        image = soup.find('img', attrs={"class":"prod_image_selector"})['src']
    except TypeError:
        try: 
            image = soup.find('img', id="main-image")['src']
        except TypeError:
            image = NO_IMAGE_URL
            pass
        pass
    
#    price = price_template.renderContents()
#    title = title_template.renderContents()
    website = string.split(".")[1]

    out = dict([('price',price),('title',title),('website',website),('image',image)])

    return out

#ebay parser - gets the title, price and website name

def ebayread(string):

    print "In EbayRead: ", string.encode('utf-8')

    article = string.encode('utf-8')

    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]

    try:
        resource = opener.open(article)
    except urllib2.URLError:
        print "Oops! Url is broken", article
        return "No info available now"
        pass
    data = resource.read()
    resource.close()

    soup = BeautifulSoup(data)

    price_template = soup.find('span',attrs={"itemprop":"price"}) 
    title_template = soup.find('h1',attrs={"class":"vi-is1-titleH1"})
    image = soup.find('span', attrs={"itemprop":"image"})['content']

    price = "$" + price_template.renderContents().split("$")[1]
    title = title_template.renderContents()

    website = string.split(".")[1]

    out = dict([('price',price),('title',title),('website',website),('image',image)])

    return out

#bestbuy parser - gets the title, price and website name

def bbuyread(string):

    print "In BbuyRead: ", string.encode('utf-8')

    article = string.encode('utf-8')

    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]

    try:
        resource = opener.open(article)
    except urllib2.URLError:
        print "Oops! Url is broken", article
        return "No info available now"
        pass
    data = resource.read()
    resource.close()

    soup = BeautifulSoup(data)

    price_template = soup.find('span',attrs={"itemprop":"price"}) 
    title_template = soup.find('h1',attrs={"itemprop":"name"})
    image = soup.find('img',attrs={"itemprop":"image"})["src"]

    price = "$" + price_template.renderContents().split("$")[1]
    title = re.sub("\n"," ",title_template.renderContents())

    website = string.split(".")[1]

    out = dict([('price',price),('title',title),('website',website),('image',image)])

    return out


#target parser - gets the title, price and website name

def targetread(string):

    print "In TargetRead: ", string.encode('utf-8')

    article = string.encode('utf-8')

    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]

    try:
        resource = opener.open(article)
    except urllib2.URLError:
        print "Oops! Url is broken", article
        return "No info available now"
        pass
    data = resource.read()
    resource.close()

    soup = BeautifulSoup(data)

    price_template = soup.find('p',attrs={"class":"price"}) 
    title_template = soup.find('span',attrs={"itemprop":"name"})
    image = soup.find('img',attrs={"itemprop":"image"})["src"]

    price = "$" + price_template.renderContents().split("$")[1]
    price = price.strip()
    title = re.sub("\n","",title_template.renderContents())

    website = string.split(".")[1]

    out = dict([('price',price),('title',title),('website',website),('image',image)])

    return out


#target parser - gets the title, price and website name

def macysread(string):

    print "In TargetRead: ", string.encode('utf-8')

    article = string.encode('utf-8')

    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]

    try:
        resource = opener.open(article)
    except urllib2.URLError:
        print "Oops! Url is broken", article
        return "No info available now"
        pass
    data = resource.read()
    resource.close()

    soup = BeautifulSoup(data)

    price_template = soup.find('span',attrs={"class":"priceSale"}) 
    title_template = soup.find('h1',attrs={"id":"productTitle"})
    image = soup.find('img', id="mainImage")['src']

    price = "$" + price_template.renderContents().split("$")[1]
    title = re.sub("\n","",title_template.renderContents())

    website = string.split(".")[1]

    out = dict([('price',price),('title',title),('website',website),('image',image)])

    return out

#Instantiate the request

url1 = "http://www.amazon.com/Fender-Starcaster-Acoustic-Natural-Guitar/dp/B000VO6DBU/ref=sr_1_6?ie=UTF8&qid=1344056560&sr=8-6&keywords=guitar"
url11 = "http://www.amazon.com/Hurley-Mens-Boardwalk-Short-Concrete/dp/B008CETOR6/ref=sr_1_1?s=apparel&ie=UTF8&qid=1344095994&sr=1-1"
url111 = "http://www.amazon.com/Apple-MacBook-MD101LL-13-3-Inch-VERSION/dp/B0074703CM/ref=zg_bs_565108_1"
url1 = "http://www.amazon.com/Kindle-Fire-Amazon-Tablet/dp/B0051VVOB2/ref=sr_tr_sr_1?ie=UTF8&qid=1344098600&sr=8-1&keywords=Kindle+Fire"
url2 = "http://www.ebay.com/itm/Fender-Squier-Waynes-World-Strat-Stratocaster-/251118402552?pt=Guitar&hash=item3a77d2bbf8#ht_500wt_1284"
url3 = "http://www.bestbuy.com/site/Acer+-+11.6%26%2334%3B+Aspire+One+Laptop+-+2GB+Memory+-+320GB+Hard+Drive+-+Ash+Black/5688602.p?id=1218684536310&skuId=5688602&st=%205688602&cp=1&lp=1"
url4 = "http://www.target.com/p/apple-16gb-ipad-2-with-wi-fi-black-mc769ll-a/-/A-13407780#?lnk=Utility_ELEC_072912_X2Y1|X2Y1&intc=X2Y1|null"
#url5 = "http://www1.macys.com/shop/product/js-collections-dress-sleeveless-ruffled-sheath?ID=673597&CategoryID=5449#fn=sp%3D1%26spc%3D1273%26ruleId%3D72%26slotId%3Drec(8)"
url5 = "http://www1.macys.com/shop/product/inc-international-concepts-dress-kimono-sleeve-empire-waist-printed?ID=679804&CategoryID=5449#fn=SPECIAL_OCCASIONS%3DCasual%26sp%3D1%26spc%3D366%26ruleId%3D72%26slotId%3D4"

dictionary = amazonread(url1)
#dictionary = ebayread(url2)
#dictionary = bbuyread(url3)
#dictionary = targetread(url4)
#dictionary = macysread(url5)

print dictionary['title'], "ON ", dictionary['website'], "HAS PRICE: ", dictionary['price'], "AND IMG_LINK: ", dictionary['image']


