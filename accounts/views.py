from django.shortcuts import render, redirect
from .forms import SignupForm

# Create your views here.
def signup(request):
    if request.method == "POST":
        forms = SignupForm(request.POST)
        if forms.is_valid():
            forms.save()
            return redirect('reviews:index')
    else:
        forms = SignupForm()
    context = {
        "forms" : forms,
    }
    return render(request, "accounts/signup.html", context)