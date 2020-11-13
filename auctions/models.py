from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
	category = models.CharField(max_length=64)

class Listing(models.Model):
	lister = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
	category = models.ForeignKey(Category, blank=True)
	title = models.CharField(max_length=64)
	description = models.TextField()
	starting_bid = models.DecimalField(max_digits=12, decimal_places=2)
	img_url = models.URLField(blank=True)
	watchers = models.ManyToManyField(User, blank=True, related_name="watched_listings")

class Bid(models.Model):
	bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
	list_item = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
	bid_amount = models.DecimalField(max_digits=12, decimal_places=2)

class Comments(models.Model):
	commenter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
	list_item = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
	comment_text = models.TextField()
