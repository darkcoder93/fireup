from django.urls import path
from . import views

app_name = 'fire_tracker'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('intro/', views.intro, name='intro'),
    path('setup/', views.setup_profile, name='setup_profile'),
    path('monthly-tracking/', views.monthly_tracking, name='monthly_tracking'),
    path('monthly-tracking/<int:tracking_id>/edit/', views.edit_monthly_tracking, name='edit_monthly_tracking'),
    path('goals/', views.goals, name='goals'),
    path('goals/<int:goal_id>/update/', views.update_goal_progress, name='update_goal_progress'),
    path('analytics/', views.analytics, name='analytics'),
    path('calculator/', views.fire_calculator, name='fire_calculator'),
    path('api/fire-progress/', views.api_fire_progress, name='api_fire_progress'),
    path('help-chat/', views.help_chat, name='help_chat'),
    path('track-visitor/', views.track_visitor, name='track_visitor'),
    path('register/', views.register, name='register'),
] 