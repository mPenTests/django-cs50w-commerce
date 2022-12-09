from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

    def __str__(self):
        return self.username
    
    
class Category(models.Model):
    category = models.CharField(max_length=100, blank=True)
    
    class Meta:
        verbose_name_plural = "Categories"
        
        
    def __str__(self):
        return self.category


class AuctionListing(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    seller = models.CharField(max_length=15, blank=True)
    title = models.CharField(max_length=100, blank=True)
    winner = models.CharField(max_length=15, blank=True)
    description = models.TextField(max_length=2000, blank=True)
    category = models.ForeignKey(Category, blank=True, on_delete=models.CASCADE)
    price = models.FloatField()
    image = models.ImageField(upload_to="images/", blank=True)
    
    def __str__(self):
        return self.title


class Bid(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    bidder = models.CharField(max_length=15, blank=True)
    auction = models.ForeignKey(AuctionListing, on_delete=models.CASCADE)
    bid = models.FloatField(default=0.00)
    
    def __str__(self):
        return str(self.id)

class Comment(models.Model):
    commenter = models.ForeignKey(User, on_delete=models.CASCADE)
    auction = models.ForeignKey(AuctionListing, on_delete=models.CASCADE)
    title = models.CharField(max_length=70, blank=True)
    comment = models.TextField(max_length=2000, blank=True)
    
    def __str__(self):
        return self.title
    
    
class Watchlist(models.Model):
    watcher = models.ForeignKey(User, on_delete=models.CASCADE)
    auction = models.ForeignKey(AuctionListing,on_delete=models.CASCADE)
    
    def __str__(self):
        return self.auction.title
    
    
