from .models import WebPage
from django.db.models import Q


def create_navbar(request, current):
    navbar = []
    this_dict = {
                 "link": "home",
                 "label": "Home",
                 "active": True if current == "home" else ""
                }
    navbar.append(this_dict)
    this_dict = {
                "link": "blog",
                "label": "Blog",
                "active": True if current == "blog" else ""
    }
    navbar.append(this_dict)
    menu_items = WebPage.objects.filter(
        Q(status=WebPage.PUBLISHED) & Q(level=1)
        ).order_by('priority')
    for m in menu_items:
        children = WebPage.objects.filter(
            Q(parent=m.id) & Q(status=WebPage.PUBLISHED)
        ).order_by('priority')
        navbar.append({
                        "label": m.title,
                        "link": "showpage",
                        "param": m.id,
                        "active": True if current == m.title else ""
                          })
        if children.count()>0:
            navbar[-1]["children"] = []
            for c in children:
                navbar[-1]["children"].append({
                    "label": c.title,
                    "link": "showpage",
                    "param": c.id,
                    "active": True if current == c.title else ""
                })
    print(navbar)
    return navbar
