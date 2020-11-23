from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
	path("create_listing", views.create_listing, name="create_listing"),
	path("listing/<list_id>", views.listing, name="listing"),
	path("make_bid/<list_id>", views.make_bid, name="make_bid"),
	path("add_watch/<list_id>", views.add_watch, name="add_watch"),
	path("remove_watch/<list_id>", views.remove_watch, name="remove_watch"),
	path("close_auction/<list_id>", views.close_auction, name="close_auction"),
	path("watchlist", views.watchlist, name="watchlist"),
	path("categories", views.categories, name="categories"),
	path("category_listings/<category_id>", views.category_listings, name="category_listings")
]
