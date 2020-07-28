from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    def __str__(self):
        return f"{self.username}: {self.email} {self.id}"


class listings(models.Model):
    name = models.CharField(max_length = 64)
    price = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="active_listings", default = "", null=True)

    def __str__(self):
        return f"{self.name}: \nPrice: {self.price} \nBy: {self.user.username}"