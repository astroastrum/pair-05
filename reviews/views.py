from django.shortcuts import redirect, render
from reviews.foms import ReviewForm
from .models import Review


# Create your views here.
def main(request):
    return render(request, "reviews/main.html")


def index(request):
    review = Review.objects.all()
    context = {"review": review}
    return render(request, "reviews/index.html", context)


def create(request):
    if request.method == "POST":
        forms = ReviewForm(request.POST)
        if forms.is_valid():
            forms.save()
            return redirect("reviews:index")

    else:
        forms = ReviewForm()
    context = {
        "forms": forms,
    }
    return render(request, "reviews/create.html", context)

def detail(request, review_pk):
    review = Review.objects.get(pk=review_pk)
    return render(request, "reviews/detail.html", {"review": review,})


def update(request, review_pk):
    review = Review.objects.get(pk=review_pk)
    if request.method == "POST":
        forms = ReviewForm(request.POST, instance=review)
        if forms.is_valid():
            forms.save()
            return redirect("reviews:detail", review_pk)

    else:
        forms = ReviewForm(instance=review)
    context = {
        "forms": forms,
    }
    return render(request, "reviews/update.html", context)