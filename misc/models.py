from django.db import models
from wagtail.models import Page


class MiscPage(Page):
    template = 'misc/miscellaneous_page.html'
    class Meta:
        verbose_name = "Miscellaneous Page"
        verbose_name_plural = "Miscellaneous Pages"
