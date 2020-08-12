from django.contrib.auth.models import AbstractUser
from django.db import models

CATEGORIES = (  
    ('FAS','Fashion'),
    ('ELC','Electronics'),
    ('TYS','Toys'),
    ('HME','Home'),
    ('ATO','Auto'),

)

class User(AbstractUser):
    def __str__(self):
        return f"{self.username}: {self.email}"


class bid(models.Model):
    bid_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bidder", default = "" , null=True)
    bid = models.IntegerField(default = 0)
    def __str__(self):
        return f"Highest bid is {self.bid} by {self.bid_by.username} "

class listings(models.Model):
    name = models.CharField(max_length = 64)
    price = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="active_listings", default = "", null=True) 
    highest_bid = models.ForeignKey(bid, on_delete=models.CASCADE, related_name="bids", default = "No current bid", null=True)
    image_file = models.CharField(max_length = 5000, blank=True)
    category    = models.CharField(max_length=3, choices = CATEGORIES, default ='Auto')
    in_watchlist = models.ManyToManyField(User, blank=True)
    description = models.TextField(default = "", blank=True)
    details = models.TextField(default = "",  blank=True)
    sold = models.BooleanField(default=False)
    def __str__(self):
        if self.highest_bid.bid_by.username == "DEFAULT":
            return f"{self.name}: Price is ${self.price} By: {self.user.username} ----- No current bid  + {self.id} "
        return f"{self.name}: Price is ${self.price} By: {self.user.username} ----- Highest bid is ${self.highest_bid.bid} by {self.highest_bid.bid_by.username} + {self.id}"



class comments(models.Model):
    listing = models.ForeignKey(listings, on_delete=models.CASCADE, related_name="item", default = "" , null=True)
    commentor =  models.ForeignKey(User, on_delete=models.CASCADE, related_name="commentor", default = "" , null=True)
    comment = models.TextField(default = "", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.listing.name}-{self.commentor.username}: {self.comment}"