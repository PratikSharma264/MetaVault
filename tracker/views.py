import json, os
from datetime import date
from django.db.models import Sum
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import FoodEntry, Profile, WaterEntry, Workout
from .serializers import FoodEntrySerializer, ProfileSerializer, WaterEntrySerializer, WorkoutSerializer

def index(request): return render(request, "index.html")

def totals():
    today = date.today()
    food = FoodEntry.objects.filter(eaten_at=today).aggregate(calories=Sum("calories"), protein=Sum("protein"), carbs=Sum("carbs"), fat=Sum("fat"))
    water = WaterEntry.objects.filter(consumed_at=today).aggregate(amount=Sum("amount_ml"))["amount"] or 0
    workout = Workout.objects.filter(completed_at=today).aggregate(amount=Sum("calories_burned"))["amount"] or 0
    return {k: float(v or 0) for k,v in food.items()} | {"water_ml": water, "burned": workout}

@api_view(["GET"])
def dashboard(request):
    profile, _ = Profile.objects.get_or_create(pk=1)
    data = totals()
    data.update({"profile": ProfileSerializer(profile).data, "recent_foods": FoodEntrySerializer(FoodEntry.objects.all()[:8], many=True).data,
                 "water_entries": WaterEntrySerializer(WaterEntry.objects.filter(consumed_at=date.today()), many=True).data})
    return Response(data)

@api_view(["GET", "PATCH"])
def profile(request):
    instance, _ = Profile.objects.get_or_create(pk=1)
    if request.method == "PATCH":
        serializer = ProfileSerializer(instance, data=request.data, partial=True); serializer.is_valid(raise_exception=True); serializer.save()
        return Response(serializer.data)
    return Response(ProfileSerializer(instance).data)

@api_view(["GET", "POST"])
def foods(request):
    if request.method == "POST":
        serializer = FoodEntrySerializer(data=request.data); serializer.is_valid(raise_exception=True); serializer.save(); return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(FoodEntrySerializer(FoodEntry.objects.all(), many=True).data)

@api_view(["DELETE"])
def food_detail(request, pk):
    try: FoodEntry.objects.get(pk=pk).delete()
    except FoodEntry.DoesNotExist: return Response(status=status.HTTP_404_NOT_FOUND)
    return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(["GET", "POST"])
def water(request):
    if request.method == "POST":
        serializer = WaterEntrySerializer(data=request.data or {"amount_ml": 250}); serializer.is_valid(raise_exception=True); serializer.save(); return Response(serializer.data, status=201)
    return Response(WaterEntrySerializer(WaterEntry.objects.filter(consumed_at=date.today()), many=True).data)

@api_view(["GET", "POST"])
def workouts(request):
    if request.method == "POST":
        serializer = WorkoutSerializer(data=request.data); serializer.is_valid(raise_exception=True); serializer.save(); return Response(serializer.data, status=201)
    return Response(WorkoutSerializer(Workout.objects.all(), many=True).data)

def ask_ai(system, prompt):
    key = os.getenv("OPENAI_API_KEY")
    if not key: return None
    try:
        from openai import OpenAI
        response = OpenAI(api_key=key).chat.completions.create(model=os.getenv("OPENAI_MODEL", "gpt-4.1-mini"), messages=[{"role":"system","content":system},{"role":"user","content":prompt}], temperature=.5)
        return response.choices[0].message.content
    except Exception: return None

@api_view(["POST"])
def ai_coach(request):
    message = request.data.get("message", "Give me a concise motivating wellness tip.")
    context = totals(); profile, _ = Profile.objects.get_or_create(pk=1)
    answer = ask_ai("You are a friendly, evidence-aware fitness coach. Never diagnose. Be concise, encouraging and practical.", f"Profile: {profile.daily_calorie_goal} kcal, {profile.daily_protein_goal}g protein goal. Today: {context}. User: {message}")
    if not answer:
        remaining = max(profile.daily_calorie_goal - context["calories"], 0)
        answer = f"You have about {remaining:.0f} calories remaining today. Prioritize a protein-rich whole-food meal and keep your next choice simple."
    return Response({"answer": answer, "powered_by_ai": bool(os.getenv("OPENAI_API_KEY"))})

@api_view(["POST"])
def analyze_food(request):
    text = request.data.get("description", "")
    result = ask_ai("Estimate nutrition from food descriptions. Return only valid JSON with name, calories, protein, carbs, fat. Use numbers and conservative estimates.", text)
    try: return Response(json.loads(result))
    except (TypeError, json.JSONDecodeError):
        return Response({"name": text or "Food item", "calories": 350, "protein": 18, "carbs": 38, "fat": 14, "estimated": True})
