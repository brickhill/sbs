from .models import WebPage, CodeSnippet
from django.db.models import Q
import re
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.styles import get_style_by_name
from pygments.formatters import HtmlFormatter


def code_snippet(snippet):
    if snippet:
        get_style_by_name("colorful")
        anchors = re.findall(r"(\[\[(\d+)\]\])", snippet)
        for a in anchors:
            snippet_record = CodeSnippet.objects.get(id=a[1])
            lexer = get_lexer_by_name("python", stripall=True)
            formatter = HtmlFormatter(linenos=True, cssclass="code-highlight")
            snippet = snippet.replace(a[0], 
                                      highlight(snippet_record.snippet,
                                      lexer, formatter
                                      ))
    
    return snippet

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
    this_dict = {
                "link": "contact",
                "label": "Contact",
                "active": True if current == "contact" else ""
    }
    navbar.append(this_dict)
    menu_items = WebPage.objects.filter(
        Q(status=WebPage.PUBLISHED) 
        & Q(level=1)
        & Q(type=WebPage.PAGE)
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
    return navbar
