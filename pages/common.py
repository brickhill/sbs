from .models import WebPage
from django.db.models import Q


def create_navbar(request, current):
    navbar = []
    this_dict = {
                 "link": "/",
                 "label": "Home",
                 "active": True if current == "home" else ""
                }
    navbar.append(this_dict)
    print("NAVBAR CREATION START")
    menu_items = WebPage.objects.filter(
        Q(status=WebPage.PUBLISHED) & Q(level=1)
        ).order_by('priority')
    for m in menu_items:
        navbar.append({
                       "label": m.title,
                       "link": f"/page/{m.id}",
                       "active": True if current == m.title else ""
                      })
    print("NAVBAR CREATION END")
    return navbar
