from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
#from django.forms import ModelForm, Form
from django import forms

from .models import User, Listing, Category, Bid, Comment

# Create class from Listings model for form to add new listing
class NewListingForm(forms.ModelForm):
	class Meta:
		model = Listing
		fields = ["title", "category", "starting_bid", "img_url", "description"]

class MakeBidForm(forms.Form):
	new_bid = forms.DecimalField(label="Bid amount: £", max_digits=12, decimal_places=2)

def index(request):

	# Get list of all active listings
	active_listings = Listing.objects.filter(is_active=True)

	return render(request, "auctions/index.html", {
		"active_listings": active_listings
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

@login_required
def create_listing(request):
	
	if request.method == "POST":
		
		# Get info from submitted form
		form = NewListingForm(request.POST)

		# Check form is valid
		if form.is_valid():
			
			new_entry = Listing()
			new_entry = form.save(commit=False) 
			current_user = User.objects.get(username=(str(request.user.username)))
			new_entry.lister = current_user
			new_entry.is_active = True
			new_entry.save()

			return render(request, "auctions/index.html")
			
	else:
		return render(request, "auctions/create_listing.html", {
			"form": NewListingForm()
		}) 

def listing(request, list_id):

	# Get listing item from list_id
	item = Listing.objects.get(id=list_id)
	
	if not item:
		return render(request, "auctions/no_item.html")

	# Bids model specifies that bids are ordered from highest to lowest by default, so this retrieves highest current bid
	current_bid = Bid.objects.filter(listing=item).first()

	# Get current user and check if they are logged in and if they are watching the current item
	current_user = request.user
	if current_user.is_authenticated:
		watched_item = current_user.watched_listings.filter(id=list_id).first()
	else:
		watched_item = None
	

	return render(request, "auctions/listing.html", {
		"item": item, "bid": current_bid, "bid_form": MakeBidForm(), "is_watched": watched_item
	})

@login_required
def make_bid(request, list_id):

	if request.method == "POST":
		bid_form = MakeBidForm(request.POST)

		if bid_form.is_valid():
			new_bid = bid_form.cleaned_data["new_bid"]
		else:
			message = "Bid is not valid"
			# Render listing page with message
			return render(request, "auctions/listing.html/" + list_id, {
				"bid_form": bid_form, "message": message
			})
		
		item = Listing.objects.get(id=list_id)
		starting_bid = item.starting_bid
		query_bid = Bid.objects.filter(listing=item).first()
		
		# Determine lowest possible bid
		if not query_bid:
			current_bid = starting_bid
		else:
			current_bid = query_bid.bid_amount

		if (new_bid <= current_bid):
			# Deal with sitution where bid is too low
			#
			# This render function doesn't work AS IS - come back and look at this
			#
			#
			message = "Error: Bid is too low"
			return HttpResponseRedirect(reverse("listing", args=[list_id]))
			return render(request, "auctions/listing.html/" + list_id, {
				"bid_form": bid_form, "message": message
			})
		else:
			# Register new bid
			register_bid = Bid(bidder=request.user, bid_amount=new_bid)
			register_bid.save()
			register_bid.listing.add(item)

			return HttpResponseRedirect(reverse("listing", args=[list_id]))
			

	# If user somehow gets to this view via method other than POST, render the index page
	return render(request, "auctions/index.html")

@login_required
def add_watch(request, list_id):
	
	if request.method == "POST":
		# Get required records
		item = Listing.objects.get(id=list_id)
		current_user = request.user

		# Add user to item's watchers and re-render
		item.watchers.add(current_user)
		return HttpResponseRedirect(reverse("listing", args=[list_id]))
	else:
		return render(request, "auctions/index.html")

@login_required
def remove_watch(request, list_id):
	
	if request.method == "POST":
		# Predictably, get required records
		item = Listing.objects.get(id=list_id)
		current_user = request.user
		
		# Remove user from item's watchers and re-render
		item.watchers.remove(current_user)
		return HttpResponseRedirect(reverse("listing", args=[list_id]))
	else:
		return render(request, "auctions/index.html")

@login_required
def close_auction(request, list_id):

	if request.method == "POST":
		
		# Get required records
		item = Listing.objects.get(id=list_id)

		if (item.is_active) and (item.lister == request.user):
			item.is_active = False
			item.save()
			
		return HttpResponseRedirect(reverse("listing", args=[list_id]))
	else:
		return render(request, "auctions/index.html")

@login_required
def watchlist(request):

	# Get list of all watched listings
	watched_listings = Listing.objects.filter(watchers=request.user)

	return render(request, "auctions/watchlist.html", {
		"watched_listings": watched_listings
	})

def categories(request):

	return render(request, "auctions/categories.html", {
		"categories": Category.objects.all()
	})

def category_listings(request, category_id):

	# Get category from category id
	current_category = Category.objects.get(id=category_id)

	# Get all listings in chosen category
	category_listings = Listing.objects.filter(category=current_category)

	return render(request, "auctions/category_listings.html", {
		"category_name": current_category.category, "category_listings": category_listings
	})
