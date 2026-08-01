from django.urls import path
from . import views

urlpatterns = [
    path("dashboard/", views.dashboard),
    path("profile/", views.profile),
    path("foods/", views.foods), path("foods/<int:pk>/", views.food_detail),
    path("water/", views.water), path("workouts/", views.workouts),
    path("ai/coach/", views.ai_coach), path("ai/analyze-food/", views.analyze_food),
]
