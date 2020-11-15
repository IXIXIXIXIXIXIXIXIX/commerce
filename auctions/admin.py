from django.contrib import admin
from .models import Listing, Comment, Bid, User, Category

# Register your models here.
admin.site.register(Listing)
admin.site.register(Comment)
admin.site.register(Bid)
admin.site.register(User)
admin.site.register(Category)
