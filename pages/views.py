from django.shortcuts import render, redirect
from django.contrib import messages
# from django.http import HttpResponse
# from django.contrib.auth.decorators import login_required
# from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .common import create_navbar
from .models import WebPage


def home(request):
    navbar = create_navbar(request, 'home')
    context = {"navbar": navbar, "header": True}
    return render(request, 'home.html', context)

def showPage(request, pk):
    page = WebPage.objects.get(id=pk)
    navbar = create_navbar(request, page.title)
    context = {"navbar": navbar, "body": page.body,
    "header": False,
    "title": page.title}
    return render(request, 'page.html', context)

def showBlog(request):
    navbar = create_navbar(request, "blog")
    context = {
        "navbar": navbar, "title": "Blog"
    }
    return render(request, 'blog.html', context)

def login_page(request):
    page = 'login'
    if request.user.is_authenticated:
        messages.info(request, "Already logged in")
        return redirect('home')
    if request.method == "POST":
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except Exception as e:
            messages.error(request, f"User doesn't exist ({e})")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.info(request, 'Logged in')
            return redirect('home')
        else:
            messages.error(request, "Username or password wrong")

    context = {'page': page}
    return render(request, "login_registration.html", context)


def logoutUser(request):
    logout(request)
    messages.info(request, 'logged out')
    return redirect('home')


def registerPage(request):
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            messages.info(request, "User Created")
            return redirect('home')
        else:
            messages.error(request, "An error occurred during registration")

    return render(request, 'login_registration.html', {'form': form})

