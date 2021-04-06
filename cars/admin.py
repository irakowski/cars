from django.contrib import admin
from .models import Car, Rating

# Registered your models for Django Admin
admin.site.register(Car)
admin.site.register(Rating)
