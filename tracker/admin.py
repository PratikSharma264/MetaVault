from django.contrib import admin
from .models import FoodEntry, Profile, WaterEntry, Workout
admin.site.register([Profile, FoodEntry, WaterEntry, Workout])
