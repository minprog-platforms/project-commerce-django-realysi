from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import User, Category, Listing, Comment, Bid
from django import forms

from .models import User

from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    active = Listing.objects.filter(active=True)
    categories = Category.objects.all()
    return render(request, "auctions/index.html", {
        "listings": active,
        "categories": categories

    })


def createlisting(request):
    if request.method == "GET":
        categories = Category.objects.all()
        return render(request, "auctions/createlisting.html", {"categories": categories})
    else:
        #data form
        title = request.POST["title"]
        description = request.POST.get("description")
        nation = request.POST["nation"]
        url_image = request.POST["url_image"]
        price = request.POST["price"]
        category =request.POST.get("category")
        #user
        user = request.user
        #catyegorydata
        categoryData = Category.objects.get(name_category = category)
        #bid
        bid = Bid(bid=float(price), user=user,)
        bid.save()
        #listing
        new_listing = Listing(
            title=title,
            description=description,
            nation=nation,
            url_image=url_image,
            price=bid,
            category=categoryData,
            beheerder=user
        )
        #save newlisting to database
        new_listing.save()
        #to index.html
        return HttpResponseRedirect(reverse(index))


def add_bid(request, id):
    user = request.user
    new_bid = request.POST["new_bid"]
    data_listing = Listing.objects.get(pk=id)
    listing_in_watchlist = request.user in data_listing.watchlist.all()
    comments = Comment.objects.filter(listing=data_listing)
    owner = request.user.username == data_listing.beheerder.username
    if int(new_bid) > data_listing.price.bid:
        bid = Bid(user=user, bid=int(new_bid))
        bid.save()
        data_listing.price = bid
        data_listing.save()
        return render(request, "auctions/listing.html", {
            "update": True,
            "listing": data_listing,
            "info": "bid is placed",
            "listing_in_watchlist": listing_in_watchlist,
            "comments": comments,
            "owner": owner,
        })
    else:
        return render(request, "auctions/listing.html", {
            "update": False,
            "listing": data_listing,
            "info": "bid is to low or something went wrong",
            "listing_in_watchlist": listing_in_watchlist,
            "comments": comments,
            "owner": owner,
        })
        

def displayCategory(request):
    if request.method == "POST":
        categoryA = request.POST["category"]
        category = Category.objects.get(name_category=categoryA)
        active = Listing.objects.filter(active=True, category=category)
        categories = Category.objects.all()
        return render(request, "auctions/index.html", {
            "listings": active,
            "categories": categories

        })

def remove_wachtlist(request, id):
    data_listing = Listing.objects.get(pk=id)
    user = request.user
    data_listing.watchlist.remove(user)
    return HttpResponseRedirect(reverse("listing", args=(id, )))


def add_wachtlist(request, id):
    data_listing = Listing.objects.get(pk=id)
    user = request.user
    data_listing.watchlist.add(user)
    return HttpResponseRedirect(reverse("listing", args=(id, )))

def listing(request, id):
    listing_data = Listing.objects.get(pk=id)
    listing_in_watchlist = request.user in listing_data.watchlist.all()
    comments = Comment.objects.filter(listing=listing_data)
    owner = request.user.username == listing_data.beheerder.username
    return render(request, "auctions/listing.html", {
        "listing": listing_data,
        "listing_in_watchlist": listing_in_watchlist,
        "comments": comments,
        "owner": owner,
    })

def close(request, id):
    data_listing = Listing.objects.get(pk=id)
    data_listing.active = False
    data_listing.save()
    comments = Comment.objects.filter(listing=data_listing)
    listing_in_watchlist = request.user in data_listing.watchlist.all()
    owner = request.user.username == data_listing.beheerder.username
    return render(request, "auctions/listing.html", {
        "listing": data_listing,
        "listing_in_watchlist": listing_in_watchlist,
        "comments": comments,
        "owner": owner,
        "update": True,
        "info": "Auction closed",
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

def display_watchlist(request):
    user = request.user
    listing = user.watchlist.all()
    return render(request, "auctions/watchlist.html", {
        "listings": listing,
    })

def add_comment(request, id):
    user = request.user
    data_listing = Listing.objects.get(pk=id)
    comment = request.POST["new_comment"]
    addComment = Comment(commenter=user, listing=data_listing, message=comment)
    addComment.save()
    return HttpResponseRedirect(reverse("listing", args=(id, )))



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
