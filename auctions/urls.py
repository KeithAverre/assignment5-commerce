from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    path("active_listings/<str:category>", views.active_listings, name="active_listings"),
    path("categories", views.categories, name="categories"),

    path("create_listing", views.create_listing, name="create_listing"),
    path("user_listings", views.user_listings, name="user_listings"),
    path("listing/<int:listing_id>", views.listing, name="listing"),
    path("watchlist/", views.watchlist, name="watchlist"),
    # path("watchlist_add/<int:listing_id>", views.watchlist_add, name="watchlist_add"),
    # path("watchlist_remove/<int:listing_id>", views.watchlist_remove, name="watchlist_remove"),
    path("watchlist_toggle/<int:listing_id>", views.watchlist_toggle, name="watchlist_toggle"),

    path("newbid/<int:listing_id>", views.newbid, name="newbid"),
    path("close/<int:listing_id>", views.close, name="close"),
    path("open/<int:listing_id>", views.open, name="open"),

    path("commment/<int:listing_id>", views.comment, name="comment"),
    path("del_comment/<int:comment_id>", views.del_comment, name="del_comment"),
    path("finalize_listing/<int:listing_id>", views.finalize_listing, name="finalize_listing"),
    path("my_wins", views.my_wins, name="my_wins"),

    path("api_watchlist_toggle/<int:listing_id>", views.api_watchlist_toggle, name = "api_watchlist_toggle"),
    path("api_watchlist_count", views.api_watchlist_count, name="api_watchlist_count"),

]
