from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,redirect
from django.urls import reverse
from django import forms
from django.contrib import messages

from . import util
from auctions.models import User,Listing, Bid, Comment

class NewListing(forms.Form):
    title = forms.CharField(label='Title', max_length=50)
    description = forms.CharField(label='Description', widget= forms.Textarea, max_length=400)
    starting_bid = forms.DecimalField(label="Starting bid")
    image_url = forms.CharField(label="Image URL", max_length=400)
    category = forms.ChoiceField(label="Category", choices=Listing.CATEGORIES)

class NewComment(forms.Form):
    description = forms.CharField(label='Description', widget= forms.Textarea, max_length=400)


def index(request):
    listings = Listing.objects.all()
    return render(request, "auctions/listings_list.html", {
        "listings": listings,
        "header": "Active listings"
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

def display_listing(request, id):
    listing_to_display = Listing.objects.get(pk=id)
    return render(request, "auctions/listing.html", {
        "listing": listing_to_display,
        "comments": listing_to_display.comments.all()
    })

def create_listing(request):   
    form = NewListing(request.POST or None)
    logged_user = request.user
    if request.method == "POST" and form.is_valid():
        new_title = form.cleaned_data['title']
        new_description = form.cleaned_data['description']
        new_starting_bid = form.cleaned_data['starting_bid']
        new_image_url = form.cleaned_data['image_url']
        new_category = form.cleaned_data['category']

        new_listing = Listing(seller = logged_user, title = new_title, description = new_description, price = new_starting_bid, image_source = new_image_url, category=new_category)
        new_listing.save()

        return display_listing(request, new_listing.id)

    return render(request, 'auctions/create_listing.html', {'form': form})

def place_bid(request, listing_id):
    if request.method == 'POST' and 'bid_amount' in request.POST:
        bid_amount = float(request.POST['bid_amount'])
        current_listing = Listing.objects.get(pk=listing_id)
        
        if bid_amount >= current_listing.price:
            bid = Bid.objects.create(
                listing=current_listing,
                bidder=request.user,
                offering_price=bid_amount
            )
            bid.save()
            current_listing.price = bid_amount
            current_listing.save()
            messages.success(request, 'Bid placed successfully!')
        else:
            messages.error(request, 'Your bid should be greater than the current highest bid.')

    return redirect('display_listing', id=listing_id)
def watchlist(request):
    current_user = request.user
    listings = Listing.objects.filter(seller=current_user)
    return render(request, "auctions/listings_list.html", {
        "listings": listings,
        "header": "Watchlist"
        })
def categories(request, key):
    
    if key != "index":
        current_category = key
        listings = Listing.objects.filter(category=current_category)
        return render(request, "auctions/listings_list.html", {
            "listings": listings,
            "header": dict(Listing.CATEGORIES).get(current_category)
        })
    else:
        return render(request,"auctions/categories.html", {
            "categories": Listing.CATEGORIES
        })
def create_comment(request, listing_id):
    form = NewComment(request.POST or None)
    logged_user = request.user
    current_listing = Listing.objects.get(id=listing_id)
    if request.method == "POST" and form.is_valid():
        new_description = form.cleaned_data['description']
        new_comment = Comment(commenter=logged_user, product=current_listing,description = new_description)
        new_comment.save()

        return display_listing(request, listing_id)

    return render(request, 'auctions/create_comment.html', {
        'form': form,
        "id": current_listing.id
        })