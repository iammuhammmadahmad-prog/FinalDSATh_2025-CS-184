from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from .forms import SignUpForm


def signup_view(request):

    if request.method == 'POST':

        form = SignUpForm(request.POST)

        if form.is_valid():

            user = form.save()

            return redirect('login')

    else:

        form = SignUpForm()

    return render(request, 'accounts/signup.html', {
        'form': form
    })


@login_required
def home_view(request):

    return render(request, 'accounts/home.html')