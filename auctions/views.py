from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
import urllib.request
from .models import *


def index(request):
    return render(request,"auctions/index.html",{
        "list": listings.objects.all()
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
    listing = listings(name = request.POST['name'], price = request.POST['price'], user = current_user, highest_bid = starting_bid, image_file = request.POST['Image_url'])
    listing.save()
    return HttpResponseRedirect(reverse("index"))
    

def bider(request, id):
    myitem = (request.user == listings.objects.get(id=id).user)
    bid_button = listings.objects.get(id=id) in listings.objects.filter(in_watchlist = request.user)
    return render(request,"auctions/item_info.html",{
        "item": listings.objects.get(id=id),
        "lower": False,
        "exists": bid_button,
        "myitem": myitem
    })

def confirm_bid(request, id):
    bid_button = listings.objects.get(id=id) in listings.objects.filter(in_watchlist = request.user)
    current_user = request.user
    myitem = (current_user == listings.objects.get(id=id).user)
    print(current_user)
    if (int(request.POST['amount']) <= int(listings.objects.get(id=id).highest_bid.bid)) or (listings.objects.get(id=id).highest_bid.bid_by == current_user):
         return render(request,"auctions/item_info.html",{
        "item": listings.objects.get(id=id),
        "lower": True,
        "exists": bid_button,
        "myitem": myitem
        })
    bid(bid_by=current_user, bid=request.POST['amount']).save()
    listings.objects.filter(id=id).update(highest_bid=bid.objects.last())
    return render(request,"auctions/item_info.html",{
        "item": listings.objects.get(id=id),
        "lower": False,
        "exists": bid_button,
        "myitem": myitem
    })
def mylistings(request):
    return render(request,"auctions/mylistings.html",{
        "list": listings.objects.filter(user = request.user)
    })
def myWatchlist(request):
    return render(request,"auctions/watchlist.html",{
        "list": listings.objects.filter(in_watchlist = request.user)
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