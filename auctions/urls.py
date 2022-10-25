from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    path("active_listings", views.active_listings, name="active_listings"),
    path("active_listings/<str:category>", views.active_listings, name="active_listings"),
    path("categories", views.categories, name="categories"),

    path("create_listing", views.create_listing, name="create_listing"),
    path("user_listings", views.user_listings, name="user_listings"),
    path("listing/<int:listing_id>", views.listing, name="listing"),
    path("watchlist/", views.watchlist, name="watchlist"),
    path("watchlist_add/<int:listing_id>", views.watchlist_add, name="watchlist_add"),
    path("watchlist_remove/<int:listing_id>", views.watchlist_remove, name="watchlist_remove"),
]
