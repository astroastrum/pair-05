from django.urls import path
from . import views

app_name = "reviews"

urlpatterns = [
    path("", views.main, name="main"),
    path("reviews/index/", views.index, name="index"),
]
