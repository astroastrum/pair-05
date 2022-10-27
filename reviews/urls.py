from django.urls import path
from . import views

app_name = "reviews"

urlpatterns = [
    path("", views.main, name="main"),
    path("reviews/index/", views.index, name="index"),
    path("reviews/create/", views.create, name="create"),
    path("reviews/<int:review_pk>/", views.detail, name="detail"),
]
