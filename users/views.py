from django.shortcuts import render, redirect
from .forms import SignUpForm, LoginForm
from .models import User
from django.db.utils import IntegrityError
from django.contrib.auth import login as log, authenticate, logout as out
from django.contrib import messages

# Create your views here.


def sign_up(request):
    """
    This view render sign_up form and allows user to create an account
    (and handle cases where an account already exists etc...)
    """
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            try:
                user = User.objects.create_user(
                    form.cleaned_data['username'],
                    form.cleaned_data['email'],
                    form.cleaned_data['password'])
            except IntegrityError:
                return render(request, 'users/register.html',
                              {"form": form, "user_exists": True})

            log(request, user)
            messages.add_message(request, messages.INFO,
                                 'Welcome home, {}'.format(user.username))
            return redirect('home')

    else:  # if request method is "get"
        form = SignUpForm()
    return render(request, 'users/register.html',
                  {"form": form, "user_exists": False})


def login(request):
    """
    This view render login form and allows user to login
    (and handle cases where an account not exists etc...)
    """
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'])
            if user is not None:
                log(request, user)
                messages.add_message(request, messages.INFO,
                                     'Welcome home, {}'.format(user.username))
                return redirect('home')
            else:
                user_exists = False
                return render(request, 'users/login.html',
                              {"form": form, 'user_exists': user_exists})
    else:
        form = LoginForm()
    return render(request, 'users/login.html',
                  {"form": form, 'user_exists': True})


def logout(request):
    """
    This view allows user to logout
    """
    out(request)
    messages.add_message(request, messages.INFO, 'Revenez vite nous voir !')
    return redirect('home')
