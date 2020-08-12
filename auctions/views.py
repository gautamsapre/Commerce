from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse
import urllib.request
from .models import *


def index(request):
    return render(request,"auctions/index.html",{
        "list": listings.objects.filter(sold = False)
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
def create(request):
    return render(request, "auctions/create_listing.html", {
    })

def register_listing(request):
    current_user = request.user
    starting_bid = bid(bid_by= current_user, bid = request.POST['price'])
    starting_bid.save()
    listing = listings(name = request.POST['name'], price = request.POST['price'], details = request.POST['details'], description = request.POST['description'], user = current_user,category = request.POST['category'], highest_bid = starting_bid, image_file = request.POST['Image_url'])
    listing.save()
    return HttpResponseRedirect(reverse("index"))
    

def bider(request, id):
    myitem = (request.user == listings.objects.get(id=id).user)
    bid_button = listings.objects.get(id=id) in listings.objects.filter(in_watchlist = request.user)
    last_bidder = (listings.objects.get(id=id).highest_bid.bid_by == request.user)
    return render(request,"auctions/item_info.html",{
        "item": listings.objects.get(id=id),
        "lower": False,
        "exists": bid_button,
        "myitem": myitem,
        "last_bidder": last_bidder,
        "comments": comments.objects.filter(listing = listings.objects.get(id = id))
    })

def confirm_bid(request, id):
    bid_button = listings.objects.get(id=id) in listings.objects.filter(in_watchlist = request.user)
    current_user = request.user
    myitem = (current_user == listings.objects.get(id=id).user)
    last_bidder = (listings.objects.get(id=id).highest_bid.bid_by == current_user)
    print(current_user)
    if ((int(request.POST['amount']) <= int(listings.objects.get(id=id).highest_bid.bid)) and listings.objects.get(id=id).highest_bid.bid_by != listings.objects.get(id=id).user):
        return render(request,"auctions/item_info.html",{
        "item": listings.objects.get(id=id),
        "lower": True,
        "exists": bid_button,
        "myitem": myitem,
        "last_bidder": last_bidder,
        "comments": comments.objects.filter(listing = listings.objects.get(id = id))
        })
    bid(bid_by=current_user, bid=request.POST['amount']).save()
    listings.objects.filter(id=id).update(highest_bid=bid.objects.last())
    return redirect('place-bid', id)
def mylistings(request):
    return render(request,"auctions/mylistings.html",{
        "list": listings.objects.filter(user = request.user, sold = False),
        "sold_list": listings.objects.filter(user = request.user, sold = True)
    })
def myWatchlist(request):
    return render(request,"auctions/watchlist.html",{
        "list": listings.objects.filter(in_watchlist = request.user,  sold = False)
    })
def insertToWatchlist(request, item_id):
    item = listings.objects.get(id=item_id)
    current_user = request.user
    item.in_watchlist.add(current_user)
    return render(request,"auctions/watchlist.html",{
        "list": listings.objects.filter(in_watchlist = request.user)
    }) 
def removeFromWatchlist(request, item_id):
    item = listings.objects.get(id=item_id)
    current_user = request.user
    item.in_watchlist.remove(current_user)
    return render(request,"auctions/watchlist.html",{
        "list": listings.objects.filter(in_watchlist = request.user)
    }) 
def closeitem(request, item_id):
    bid_button = listings.objects.get(id=item_id) in listings.objects.filter(in_watchlist = request.user)
    myitem = (request.user == listings.objects.get(id=item_id).user)
    last_bidder = (listings.objects.get(id=item_id).highest_bid.bid_by == request.user)
    listings.objects.filter(id=item_id).update(sold = True)
    return render(request,"auctions/item_info.html",{
    "item": listings.objects.get(id=item_id),
    "lower": False,
    "exists": bid_button,
    "myitem": myitem,
    "last_bidder": last_bidder,
    "comments": comments.objects.filter(listing = listings.objects.get(id = item_id))
    })
def add_comment(request, item_id):
    comments(comment=request.POST['comment'], commentor = request.user, listing = listings.objects.get(id = item_id)).save()
    return HttpResponseRedirect(reverse("place-bid", args=(item_id)))
def browse_categories(request):
    return render(request, "auctions/categories.html")
def cat_listings(request, cat):
    return render(request,"auctions/index.html",{
        "list": listings.objects.filter(sold = False, category = cat),
        "cat": cat
    })