from django.db import models

class Profile(models.Model):
    name = models.CharField(max_length=80, default="Alex")
    daily_calorie_goal = models.PositiveIntegerField(default=2200)
    daily_protein_goal = models.PositiveIntegerField(default=150)
    daily_water_goal = models.PositiveIntegerField(default=8)
    streak = models.PositiveIntegerField(default=12)

    def __str__(self): return self.name

class FoodEntry(models.Model):
    MEALS = [("breakfast", "Breakfast"), ("lunch", "Lunch"), ("dinner", "Dinner"), ("snack", "Snack")]
    name = models.CharField(max_length=120)
    meal = models.CharField(max_length=12, choices=MEALS)
    calories = models.PositiveIntegerField()
    protein = models.DecimalField(max_digits=6, decimal_places=1, default=0)
    carbs = models.DecimalField(max_digits=6, decimal_places=1, default=0)
    fat = models.DecimalField(max_digits=6, decimal_places=1, default=0)
    eaten_at = models.DateField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta: ordering = ["-created_at"]

class WaterEntry(models.Model):
    amount_ml = models.PositiveIntegerField(default=250)
    consumed_at = models.DateField(auto_now_add=True)

class Workout(models.Model):
    title = models.CharField(max_length=120)
    duration_minutes = models.PositiveIntegerField()
    calories_burned = models.PositiveIntegerField(default=0)
    completed_at = models.DateField(auto_now_add=True)
