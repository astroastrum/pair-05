from django.shortcuts import render
from .models import Review

# Create your views here.
def main(request):
    return render(request, "reviews/main.html")


def index(request):
    review = Review.objects.all()
    context = {
        'review': review
    }
    return render(request, "reviews/index.html", context)