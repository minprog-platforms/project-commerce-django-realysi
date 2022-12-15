from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import User, Category, Listing
from django import forms

from .models import User


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
        #listing
        new_listing = Listing(
            title=title,
            description=description,
            nation=nation,
            url_image=url_image,
            price=float(price),
            category=categoryData,
            beheerder=user
        )
        #save newlisting to database
        new_listing.save()
        #to index.html
        return HttpResponseRedirect(reverse(index))


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
