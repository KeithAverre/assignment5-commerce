from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import User, Listing, bid, Comment
from .forms import ListingForm
from django.contrib import messages
from django.http import Http404

"""
TEMPLATE

TODO:


Known bugs:

"""


def index(request):

    return render(request, "auctions/index.html", {
        "listings": Listing.objects.filter(closed=False)
    })


def active_listings(request, category):

    return render(request, "auctions/index.html", {
        "listings": Listing.objects.filter(categories=category, closed=False),
    })


"""
This is a method to create a listing.
"""


def create_listing(request):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        if request.method == "POST":
            listing_form = ListingForm(request.POST,request.FILES)
            if listing_form.is_valid():
                # thank you kevin, you are a life saver
                new_listing = listing_form.save(commit=False)
                new_listing.user_owner = request.user
                new_listing.save()
                messages.success(request, (f'\"{listing_form.cleaned_data["title"]}\" was successfully added!'))
                return redirect("listing", listing_id=new_listing.pk)  # should go to new listing
            else:
                messages.error(request, 'Error saving form')
        else:
            listing_form = ListingForm()
        return render(request, "auctions/create_listing.html", {'listings_form': listing_form})



"""
This is a view to allow viewing of a particular listing
"""
def listing(request, listing_id):
    try:
        entry = Listing.objects.get(pk=listing_id)
    except Listing.DoesNotExist:
        raise Http404("Listing not found")
    if not request.user.is_authenticated:
        comments = Comment.objects.filter(listing=entry)
        return render(request, "auctions/listing.html", {
            "listing": entry,
            "Comments": comments,
        })
    else:
        comments = Comment.objects.filter(listing=entry)
        return render(request, "auctions/listing.html", {
            "listing": entry,
            "Comments":comments,
        })

"""
All listings by the particular user
"""
def user_listings(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.filter(user_owner=request.user),
    })


def categories(request):
    if request.method == "POST":
        return redirect(f'active_listings/{request.POST["Category"]}')  # not the prettiest solution but it works
    else:
        return render(request, "auctions/categories.html")


def newbid(request, listing_id):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        #wow that listing_id trick was from a fever dream, both the listing_id and storing the reference
        #       of how much the new bid is from listing_template
        new = bid.objects.create(bidder=request.user, amount=request.POST[f'{listing_id}'],
                           listing=Listing.objects.get(pk=listing_id))
        new.save()

        entry = Listing.objects.get(pk=listing_id)
        entry.update_bid(new.amount,new.bidder)
        entry.save()

        return redirect('listing', listing_id=listing_id)

"""
Views for management of a listing
"""
def close(request, listing_id):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        entry = Listing.objects.get(pk=listing_id)
        if request.user != entry.user_owner:
            return redirect('listing', listing_id=listing_id) #no idea how'd you get here but just in case
        else:
            entry.close_listing()
            entry.save()
            return redirect('listing', listing_id=listing_id)
def open(request, listing_id):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        entry = Listing.objects.get(pk=listing_id)
        if request.user != entry.user_owner:
            return redirect('listing', listing_id=listing_id) #no idea how'd you get here but just in case
        else:
            if entry.finalized == True:
                return redirect('listing', listing_id=listing_id)
            else:
                entry.open_listing()
                entry.save()
                return redirect('listing', listing_id=listing_id)


def finalize_listing(request, listing_id):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        entry = Listing.objects.get(pk=listing_id)
        if request.user != entry.user_owner:
            return redirect('listing', listing_id=listing_id) #no idea how'd you get here but just in case
        else:
            try:
                entry.finalize_listing(bid.objects.get(amount=Listing.objects.get(pk=listing_id).bid,listing=listing_id).bidder)
            except:
                entry.close_listing()
            entry.save()
            return redirect('listing', listing_id=listing_id)

"""
Wins for the current user
"""
def my_wins(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.filter(final_bidder=request.user),
    })



"""
This is the watchlist of the current user  
"""
def watchlist(request):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        listings = []
        for i in request.user.watch():
            listings.append(Listing.objects.get(pk=i))
        return render(request, "auctions/watchlist.html", {
            "listings": listings,
            "amount" : len(listings),
        })


def watchlist_add(request, listing_id):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        watch = request.user.watch()
        if listing_id in watch:
            return redirect('watchlist')
        else:
            request.user.add_to_watchlist(listing_id)
            request.user.save()
        return redirect('watchlist')


def watchlist_remove(request, listing_id):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        watch = request.user.watch()
        if listing_id in watch:
            request.user.remove_from_watchlist(listing_id)
            request.user.save()
        return redirect('watchlist')
def watchlist_toggle(request,listing_id):
    if request.user.is_authenticated:
        try:
            Listing.objects.get(pk=listing_id)
        except Listing.DoesNotExist:
            raise Http404("Listing not found")
        if listing_id in request.user.watch():
            request.user.remove_from_watchlist(listing_id)
            request.user.save()
        else:
            request.user.add_to_watchlist(listing_id)
            request.user.save()
        return redirect('watchlist')

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

@csrf_exempt
def api_watchlist_toggle(request,listing_id):
    if request.user.is_authenticated:
        isInWatchlist = 0
        try:
            Listing.objects.get(pk=listing_id)
        except Listing.DoesNotExist:
            raise Http404("Listing not found")
        if listing_id in request.user.watch():
            request.user.remove_from_watchlist(listing_id)
            request.user.save()
        else:
            request.user.add_to_watchlist(listing_id)
            request.user.save()
            isInWatchlist = 1
        return JsonResponse({"isInWatchlist":isInWatchlist,
                             "watchlist_count":len(request.user.watch())})
    return JsonResponse({"isInWatchlist":0})
def api_watchlist_count(request):
    if request.user.is_authenticated:
        return JsonResponse({
            "watchlist_count": len(request.user.watch())})
    else:
        return JsonResponse({
            "watchlist_count": 0})

"""
Comment views for listings well
"""
def comment(request,listing_id):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        Comment.objects.create(commenter=request.user, comment=request.POST["comment_text"],
                               listing=Listing.objects.get(pk=listing_id))

        return redirect('listing', listing_id=listing_id)
def del_comment(request, comment_id):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        if(request.user == Comment.objects.get(pk=comment_id).commenter or request.user == Comment.objects.get(pk=comment_id).listing.user_owner):

            old_comment = Comment.objects.get(pk=comment_id)
            listing_id= old_comment.listing.pk
            old_comment.delete()
            return redirect('listing', listing_id=listing_id)
        else:
            return redirect('index')  # no idea how'd you get here but just in case



"""
This is the login section for users
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
