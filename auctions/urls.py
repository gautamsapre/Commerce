from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("<id>/place-bid", views.bider, name="place-bid"),
    path("create-listing", views.create, name="create-listing"),
    path("register-listing", views.register_listing, name ="register_listing"),
    path("<id>/confirm_bid", views.confirm_bid, name ="confirm_bid"),
    path("my-listings", views.mylistings, name = "my-listings"),
    path("my-watchlist", views.myWatchlist, name ="my-watchlist"),
    path("<item_id>/insert_watchlist", views.insertToWatchlist, name = "insert_watchlist"),
    path("<item_id>/removefrom_watchlist", views.removeFromWatchlist, name = "removefrom_watchlist"),
    path("<item_id>/close-item", views.closeitem, name = "close-item")
]
