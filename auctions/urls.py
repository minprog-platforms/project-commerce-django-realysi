from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("createlisting", views.createlisting, name="createlisting"),
    path("displayCategory", views.displayCategory, name="displayCategory"),
    path("listing/<int:id>", views.listing, name="listing"),
    path("remove_watchlist/<int:id>", views.remove_wachtlist, name="remove_watchlist"),
    path("add_watchlist/<int:id>", views.add_wachtlist, name="add_watchlist"),
    path("watchlist", views.display_watchlist, name="watchlist"),
    path("comment/<int:id>", views.add_comment, name="add_comment"),
    path("add_bid<int:id>", views.add_bid, name="add_bid"),
]
