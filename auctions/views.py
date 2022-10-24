from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import User

"""
TEMPLATE

TODO:


Known bugs:

"""



def index(request):
    return render(request, "auctions/index.html")
"""
This is a method to view all listings.

TODO:
    -Add url. **Finished, needs testings xx

    -if not logged in, cannot add to watchlist
    -if filtered then 
Known bugs:

"""
def active_listings(request):
    pass

def active_listings(request,catagories):
    pass
"""
This is a method to create a listing.

TODO:
    -Add url. **Finished, needs testings xx
    -Ability to edit listing?
    -Only shown when logged in.

Known bugs:

"""
@login_required
def create_listing(request):
    pass


"""
This is a view to allow viewing of a particular listing

TODO:
    -add url + necessary string input. **Finished, needs testings xx
    
    IF LOGGED IN:
        -Allow for user to add to watchlist
        -Allow for user to bid listing

    IF NOT LOGGED IN:
        -put login button rather than bid button

Known bugs:

"""
def listing(request, listing):
    pass

"""
This is the categories view.
Allowing for a selection of categories to filter listings.

TODO:
    -Add url. **Finished, needs testings xx
    
    -how to pass in selected categories from html

Known bugs:
    
"""
def categories(request):
    pass





"""
This is the watchlist of the current user

TODO:
    -Add url. **Finished, needs testings xx
    
    -Only shown when logged in.

Known bugs:
    
"""
@login_required
def watchlist(request):
    pass







"""
This is the login section of the views.

TODO:
    -HOW TO ADD USER IN ADMIN PAGE??? SEE MODELS.PY USER.

Known bugs:
    -Registration can happen without email or password. **fixed by adding a required field to register.html
"""
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
