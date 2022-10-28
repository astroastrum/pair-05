from xml.etree.ElementTree import Comment
from django.shortcuts import redirect, render, get_object_or_404
from reviews.forms import ReviewForm, CommentForm
from .models import Review
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.db.models import Q

# Create your views here.
def main(request):
    return render(request, "reviews/main.html")


def index(request):
    review = Review.objects.all()
    context = {"review": review}
    return render(request, "reviews/index.html", context)


@login_required
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
        "forms": forms,
    }
    return render(request, "reviews/detail.html", context)


@login_required
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


@login_required
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


def search(request):
    if request.method == "GET":
        content_list = Review.objects.all()
        search = request.GET.get("search", "")

        if search:
            search_list = content_list.filter(
                Q(title__icontains=search)
                | Q(content__icontains=search)
                | Q(subtitle__icontains=search)
            )
            return render(request, "reviews/search.html", {"search": search_list})


@login_required
def comments(request, review_pk):
    if request.method == "POST":
        if request.user.is_authenticated:
            forms = CommentForm(request.POST)
            if forms.is_valid():
                comment = forms.save(commit=False)
                comment.user = request.user
                comment.save()
                return redirect("reviews:detail", review_pk)


@login_required
def comments_delete(request, review_pk, comment_pk):
    if request.method == "POST":
        # 댓글 작성자만 삭제 가능
        comment = get_object_or_404(Comment, pk=comment_pk)
        if request.user == comment.user:
            comment.delete()
    # GET으로 요청했을 경우 반응 없게
    return redirect("reviews:detail", review_pk)
