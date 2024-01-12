from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("place_bid/<int:listing_id>/", views.place_bid, name="place_bid"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("categories/<str:key>/", views.categories, name="categories"),
    path("create_comment/<int:listing_id>/", views.create_comment, name="create_comment"),
    path("<int:id>", views.display_listing, name="display_listing")
]
