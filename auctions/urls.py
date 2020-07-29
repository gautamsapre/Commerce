from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("<name>/place-bid", views.bider, name="place-bid"),
    path("create-listing", views.create, name="create-listing"),
    path("register-listing", views.register_listing, name ="register_listing")
]
