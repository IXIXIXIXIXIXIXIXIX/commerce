from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
	category = models.CharField(max_length=64, related_name="categories")

class Listing(models.Model):
	lister = models.ForeignKey(User, on_delete=models.CASCADE)
	category = models.ManyToManyField(Category, blank=True)
	title = models.CharField(max_length=64, related_name="listings")
	description = models.TextField()
	starting_bid = models.DecimalField(max_digits=12, decimal_places=2)
	img_url = models.URLField(blank=True)
	
