from django.shortcuts import redirect, render
from reviews.foms import ReviewForm, CommentForm
from .models import Review
from django.http import HttpResponseForbidden

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
    forms = CommentForm()
    context = {
            "review": review,
            "forms" : forms,
        }
    return render(request, "reviews/detail.html", context)



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


def delete(request, review_pk):
    review = Review.objects.get(pk=review_pk)
    review.delete()
    return redirect("reviews:index")


def likes(request, review_pk):
    if request.user.is_authenticated:
        review = Review.objects.get(pk=review_pk)

        if review.like_user.filter().exists():
            review.like_user.remove(request.user)
        else:
            review.like_user.add(request.user)
        return redirect("reviews:detail", review_pk)
    else:
        return HttpResponseForbidden()


def comments(request, review_pk):
    if request.method == "POST":
        if request.user.is_authenticated:
            forms = CommentForm(request.POST)
            if forms.is_valid():
                comment = forms.save(commit=False)
                comment.user = request.user
                comment.save()
                return redirect("reviews:detail", review_pk)