from django.urls import path
from . import views

app_name = "reviews"

urlpatterns = [
    path("", views.main, name="main"),
    path("reviews/index/", views.index, name="index"),
    path("reviews/create/", views.create, name="create"),
    path("reviews/<int:review_pk>/", views.detail, name="detail"),
    path("reviews/<int:review_pk>/update", views.update, name="update"),
    path("reviews/<int:review_pk>/delete", views.delete, name="delete"),
    path("reviews/<int:review_pk>/likes", views.likes, name="likes"),
    path("reviews/<int:review_pk>/comments", views.comments, name="comments"),
]
