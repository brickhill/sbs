from django.shortcuts import render, redirect
from django.contrib import messages
# from django.http import HttpResponse
# from django.contrib.auth.decorators import login_required
# from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from .common import create_navbar, code_snippet
from .models import WebPage, BlogPost


def home(request):
    navbar = create_navbar(request, 'home')
    context = {"navbar": navbar, "header": True}
    return render(request, 'home.html', context)


def showPost(request, pk):
    post = BlogPost.objects.get(id=pk)
    navbar = create_navbar(request, None)
    body = code_snippet(post.body)
    # TODO Add categories to blog post.
    cards = []
    if post.categories.all():
        cards.append({"type": "cat", "title": "Categories", "list": post.categories.all()})
    cards.append({"type": "card", "title": "Title 1", "body": "Body 1", "link": "link1"})
    cards.append({"type": "card", "title": "Title 2", "body": "Body 2", "link": "link2"})

    context = {
        "navbar": navbar,
        "body": body,
        "cards": cards,
        "header": False,
        "title": post.title
    }
    return render(request, 'post.html', context)


def showPage(request, pk):
    page = WebPage.objects.get(id=pk)
    navbar = create_navbar(request, page.title)
    body = code_snippet(page.body)
    context = {
               "navbar": navbar, "body": body,
               "header": False,
               "title": page.title
              }
    return render(request, 'page.html', context)


def terms(request):
    termsPage = WebPage.objects.filter(type=WebPage.TERMS)
    termsText = termsPage[0].body if termsPage else 'T&C coming soon'
    navbar = create_navbar(request, None)
    context = {
               "navbar": navbar,
               "body": termsText,
               "header": False,
               "title": "Terms & Conditions"
              }
    return render(request, 'page.html', context)


def privacy(request):
    termsPage = WebPage.objects.filter(type=WebPage.PRIVACY)
    termsText = termsPage[0].body if termsPage else 'Privacy coming soon'
    navbar = create_navbar(request, None)
    context = {
               "navbar": navbar, "body": termsText, "header": False,
               "title": "Privacy Policy"
              }
    return render(request, 'page.html', context)


def showBlog(request):
    navbar = create_navbar(request, "blog")
    cards = []
    print(f"CARDS TYPE {type(cards)}")
    cards.append({
                  "type": "card",
                  "title": "Title 1", 
                  "body": "Body 1", "link": "link1"
                  })
    cards.append({"type": "card",
        "title": "Title 2", "body": "Body 2", "link": "link2"})
    posts = BlogPost.objects.filter(
        status=BlogPost.PUBLISHED).order_by("-updated")
    paginator = Paginator(posts, 3)  # Show 3 results per page
    page_number = request.GET.get('page')
    posts_obj = paginator.get_page(page_number)
    context = {
        "navbar": navbar, "title": "Blog", "posts": posts_obj, "cards": cards
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
