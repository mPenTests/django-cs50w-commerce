from django.contrib import admin
from .models import AuctionListing, Bid, Comment, User, Watchlist, Comment, Category

# Register your models here.

admin.site.register(AuctionListing)
admin.site.register(Comment)
admin.site.register(Bid)
admin.site.register(User)
admin.site.register(Watchlist)
admin.site.register(Category)
