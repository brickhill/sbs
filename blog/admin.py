# from wagtail.contrib.modeladmin.options import (
#     ModelAdmin, modeladmin_register)
from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet

from .models import BlogPost


# @register_snippet
class BlogPostAdmin(SnippetViewSet):
    model = BlogPost
    menu_label = "Blog Posts"
    menu_icon = "placeholder"
    menu_order = 290
    add_to_settings_menu = False
    exclude_from_explore = False
    list_display = ("title",)
    search_fields = ("title", "body", "extract")
