from django.contrib import admin
from .models import User, listings
# Register your models here.
admin.site.register(listings)
admin.site.register(User)