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
	bid = Bid.objects.filter(listing=list_id).first()

	if not item:
		return render(request, "auctions/no_item.html")
	
	return render(request, "auctions/listing.html", {
		"item": item, "bid": bid, "bid_form": MakeBidForm()
	})

@login_required
def bid(request, list_id):

	return render(request, "auctions/index.html")
