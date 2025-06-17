from django.urls import path
from .views import suggest_titles

urlpatterns = [
    path('suggest-titles/', suggest_titles, name='suggest-titles'),
]