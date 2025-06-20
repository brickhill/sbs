from django.shortcuts import render, redirect
from django.contrib import messages
# from django.http import HttpResponse
# from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from .common import create_navbar, code_snippet
from .models import WebPage, BlogPost, Category, BlogPostSeries
from .forms import SearchSite, LoginPage, ContactForm
from itertools import chain


def home(request):
    navbar = create_navbar(request, 'home')
    context = {"navbar": navbar, "header": True}
    return render(request, 'home.html', context)


def showCategory(request, pk):
    category = Category.objects.get(id=pk)
    navbar = create_navbar(request, None)
    cards = []
    form = SearchSite()
    cards.append({"type": "search", "title": "Search", "form": form,
                  "link": "searchsite"})
    cards.append({"type": "cat", "title": "Categories",
                  "list": Category.objects.all()})
    context = {
        "navbar": navbar,
        "category": category,
        "posts": BlogPost.objects.filter(categories=category),
        "cards": cards,
        "header": False,
        "title": category.title
    }
    return render(request, 'blog.html', context)


def showPost(request, pk):
    post = BlogPost.objects.get(id=pk)
    navbar = create_navbar(request, None)
    body = code_snippet(post.body)
    cards = []
    cards.append({"type": "cat", "title": "Categories",
                  "list": Category.objects.all()})
    series = BlogPostSeries.objects.filter(id=pk)
    for s in series:
        cards.append({"type": "series", "title": s.series,
                      "list": s.series.blogpostseries_set.all().
                      order_by('priority')
                      })
    form = SearchSite()
    cards.append({"type": "search", "title": "Search", "form": form,
                  "link": "searchsite"})
    cards.append({"type": "card", "title": "Title 2", "body": "Body 2",
                  "link": "link2"})

    context = {
        "navbar": navbar,
        "post": post,
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
    form = SearchSite()
    cards.append({"type": "search", "title": "Search", "form": form,
                  "link": "searchsite"})
    cards.append({"type": "cat", "title": "Categories",
                  "list": Category.objects.all()})
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
    form = LoginPage
    context = {'page': page, 'form': form}
    return render(request, "login_registration.html", context)


def logoutUser(request):
    logout(request)
    messages.info(request, 'logged out')
    return redirect('home')


def search(request):
    # TODO Add pages to search.
    search_string = request.POST['query']
    navbar = create_navbar(request, "search")
    cards = []
    results = BlogPost.objects.filter(Q(title__icontains=search_string) |
                                      Q(body__icontains=search_string)). \
        order_by("-updated")
    page_results = WebPage.objects.filter(Q(title__icontains=search_string) |
                                      Q(body__icontains=search_string)). \
        order_by("-updated")
    results = list(chain(results, page_results))
    for r in results:
        print(f"NOB:{r.__class__.__name__}")
    paginator = Paginator(results, 3)  # Show 3 results per page
    page_number = request.GET.get('page')
    results_obj = paginator.get_page(page_number)
    context = {
        "navbar": navbar,
        "title": "Blog",
        "results": results_obj,
        "cards": cards,
        'query': search_string
    }
    return render(request, 'search.html', context=context)


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


def contactForm(request):
    navbar = create_navbar(request, "contact")
    cards = []
    form = ContactForm()
    print(f"FORM:{str(form)}")
    context = {
        "navbar": navbar,
        "title": "Contact",
        "cards": cards,
        "form": form
    }
    return render(request, 'contact.html', context=context)
