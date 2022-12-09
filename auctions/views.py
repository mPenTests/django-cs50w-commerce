from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .forms import AuctionListingForm, CommentForm
from .models import User, AuctionListing, Bid, Watchlist, Comment, Category
from django.contrib.auth.decorators import login_required


def index(request, auctions=False):
    if auctions:
        objects = []
        
        for auction in auctions:
            objects.append(AuctionListing.objects.get(title=auction))
        
        return render(request, "auctions/index.html", {
            "auctions": objects
        })  
          
    return render(request, "auctions/index.html", {
        "auctions": AuctionListing.objects.all()
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
    
    
def categories(request):
    categories = Category.objects.all()
    
    return render(request, "auctions/categories.html", {
        "categories": categories
    })
    
    
@login_required(login_url="/login")
def create(request):
    form = AuctionListingForm()
    categories = Category.objects.all()
    
    if request.method == "GET":
        return render(request, "auctions/create.html", {
            "form":form,
            "categories":categories
        })
        
    elif request.method == "POST":
        titl = request.POST.get("title")
        desc = request.POST.get("description")
        prc = request.POST.get("price")
        img = request.FILES.get("image")
        sellr = request.user.username
        categry = request.POST.get("category")
        print(categry)
        
        form1 = AuctionListing(seller=sellr, title=titl, description=desc, price=prc, image=img, category=Category.objects.get(category=categry))
        
        form1.save()
    
    return HttpResponseRedirect(reverse("index"))


@login_required(login_url="/login")
def showListing(request, id, message=False):
    global comment_form
    listing = AuctionListing.objects.get(pk=id)
    comment_form = CommentForm()
    comments = Comment.objects.filter(auction=listing)
    close = False
    
    if listing.seller == request.user.username:
        close = True
    
    return render(request, "auctions/listing.html", {
        "object": listing,
        "image": listing.image.url,
        "message": message,
        "commentform": comment_form,
        "comments": comments,
        "close": close, 
        "winner": listing.winner
    })
    

@login_required(login_url="/login")
def placeBid(request, id):
    bid = request.POST["bid"]
    object = AuctionListing.objects.get(pk=id)
    current_price = object.price
    
    if float(bid) < float(current_price):
        error = "Bid is lower than current price."
        return showListing(request, id, error)
        
    else:
        placed_bid = Bid(bidder=request.user.username, auction=AuctionListing.objects.get(pk=id), bid=float(bid))
        object.price = float(bid)
        
        placed_bid.save()
        object.save(update_fields=["price"])
        return index(request)
    
    
@login_required(login_url="/login")
def showWatchlist(request):
    error = False
    watchlist = Watchlist.objects.filter(watcher=User.objects.get(username=request.user.username))
    queryset = []
    objects = []
    
    if len(watchlist) < 1:
        error = True
    
    else:
        for item in watchlist:
            queryset.append(item)
            
        for query in queryset:
            tmp = AuctionListing.objects.get(title=query)
            objects.append(tmp)
            
    return render(request, "auctions/watchlist.html", {
        "items": objects,
        "error": error
    })
    
    
@login_required(login_url="/login")
def removeWatchlist(request, item_id):
    item = Watchlist.objects.get(watcher=User.objects.get(username=request.user.username), auction=AuctionListing.objects.get(pk=item_id))
    item.delete()
        
    return HttpResponseRedirect(reverse("showWatchlist"))


@login_required(login_url="/login")
def addWatchlist(request, auction_id):
    # Remove Duplicates -- start
    
    for i in Watchlist.objects.all():
        _ = AuctionListing.objects.get(title=i)
        
        if _.id == auction_id:
            i.delete()
    
    # Remove duplicates -- end
            
    watchlist = Watchlist(watcher=User.objects.get(username=request.user.username), auction=AuctionListing.objects.get(pk=auction_id))
    watchlist.save()  
   
    return HttpResponseRedirect(reverse("showWatchlist"))


@login_required(login_url="/login")
def comment(request, auction_id):
    if request.method == "POST":
        auction = AuctionListing.objects.get(pk=auction_id)
        title = request.POST["title"]
        comment = request.POST["comment"]
        
        cmment = Comment(commenter=User.objects.get(username=request.user.username), auction=auction, title=title, comment=comment)
        cmment.save()
        
        return HttpResponseRedirect(reverse('show', args=(auction_id,)))
    
    
@login_required(login_url="/login")
def showCatItems(request, category):
    auctions = AuctionListing.objects.filter(category=Category.objects.get(category=category))
    
    return index(request, auctions=auctions)


@login_required(login_url="/login")
def close(request, auction_id):
    auction = AuctionListing.objects.get(pk=auction_id)
    bids = Bid.objects.filter(auction=auction)
    ids = []
    
    for id in bids:
        ids.append(str(id).strip("<Bid: >"))
        
    tmp = 0
    winner = ""
    
    for i in ids:
        j = Bid.objects.get(pk=i)
        if j.bid > tmp:
            tmp = j.bid
            auction.winner = j.bidder
            auction.save(force_update=True)
            
    return showListing(request, auction_id)