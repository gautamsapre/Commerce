from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    def __str__(self):
        return f"{self.username}: {self.email} {self.id}"


class bid(models.Model):
    bid_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bidder", default = "", null=True)
    bid = models.IntegerField()

    def __str__(self):
        return f"Highest bit is {self.bid} by {self.bid_by}"

class listings(models.Model):
    name = models.CharField(max_length = 64)
    price = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="active_listings", default = "", null=True) 
    highest_bid = models.ForeignKey(bid, on_delete=models.CASCADE, related_name="bids", default = "No current bid", null=True)
    
    def __str__(self):
        return f"{self.name}: \nPrice: {self.price} \nBy: {self.user.username}"