from django.db import models
from modelcluster.models import ClusterableModel
from modelcluster.fields import ParentalKey
from django_extensions.db.fields import AutoSlugField
from wagtail.admin.panels import FieldPanel, PageChooserPanel, InlinePanel
from wagtail.models import Orderable


class MenuItem(Orderable):
    link_title = models.CharField(max_length=50, blank=True)
    link_url = models.CharField(max_length=500, blank=True)
    link_page = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        related_name="+",
        on_delete=models.CASCADE
    )
    open_in_new_tab = models.BooleanField(blank=True, default=False)
    panels = [
        FieldPanel("link_title"),
        FieldPanel("link_url"),
        PageChooserPanel("link_page"),
        FieldPanel("open_in_new_tab")
    ]

    page = ParentalKey("Menu", related_name="menu_items")

    @property
    def link(self) -> str:
        if self.link_page:
            return self.link_page.url
        elif self.link_url:
            return self.link_url
        else:
            return '#'

    @property
    def title(self)->str:
        if self.link_page and not self.link_title:
            return self.link_page.title
        elif self.link_title:
            return self.link_title
        return "No Title"



class Menu(ClusterableModel):
    title = models.CharField(max_length=100)
    slug = AutoSlugField(
        populate_from="title",
        editable=True
    )

    panels = [
        FieldPanel("title"),
        FieldPanel("slug"),
        InlinePanel("menu_items", label="Menu Item")
    ]

    def __str__(self):
        return self.title
