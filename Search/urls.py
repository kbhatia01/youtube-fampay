from django.contrib import admin
from django.urls import path
from .views import YoutubeVideoView


urlpatterns = [
    path('youtube/', YoutubeVideoView.as_view())
]
