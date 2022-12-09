from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("categories", views.categories, name="categories"),
    path("create", views.create, name="create"),
    path("show/<int:id>", views.showListing, name="show"),
    path("place/<int:id>", views.placeBid, name="place"),
    path("showWatchlist", views.showWatchlist, name="showWatchlist"),
    path("removeWatchlisting/<int:item_id>", views.removeWatchlist, name="remove"),
    path("addWatchlist/<int:auction_id>", views.addWatchlist, name="addWatchlist"),
    path("comment/<int:auction_id>", views.comment, name='comment'),
    path("showCatItems/<str:category>", views.showCatItems, name="showCatItems"),
    path("close/<int:auction_id>", views.close, name="close")
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)