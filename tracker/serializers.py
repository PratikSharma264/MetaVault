from rest_framework import serializers
from .models import FoodEntry, Profile, WaterEntry, Workout

class FoodEntrySerializer(serializers.ModelSerializer):
    class Meta: model = FoodEntry; fields = "__all__"; read_only_fields = ("eaten_at", "created_at")
class WaterEntrySerializer(serializers.ModelSerializer):
    class Meta: model = WaterEntry; fields = "__all__"; read_only_fields = ("consumed_at",)
class WorkoutSerializer(serializers.ModelSerializer):
    class Meta: model = Workout; fields = "__all__"; read_only_fields = ("completed_at",)
class ProfileSerializer(serializers.ModelSerializer):
    class Meta: model = Profile; fields = "__all__"
