from django.db import models
from wagtail.models import Page
from wagtail.admin.panels import FieldPanel, PageChooserPanel
from django.core.exceptions import ValidationError


class ServiceListingPage(Page):
    subtitle = models.TextField(blank=True, max_length=500)

    content_panels = Page.content_panels + [
        FieldPanel("subtitle")
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context['services'] = ServicePage.objects.live().public
        import pudb
        pu.db()
        pg = 'PG'
        return context


class ServicePage(Page):

    template = "services/service_page.html"
    description = models.TextField(max_length=500, blank=True)
    internal_page = models.ForeignKey(
        'wagtailcore.Page', on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='+', help_text="Select internal page"
    )
    external_page = models.URLField(blank=True)
    button_text = models.CharField(max_length=500,
                                   blank=True, help_text="Button Text")
    service_image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.SET_NULL, null=True,
        related_name='+', blank=False,
        help_text="image on service listing page.  Will be cropped 570x370")

    content_panels = Page.content_panels + [
        FieldPanel("title"),
        FieldPanel("description"),
        PageChooserPanel("internal_page"),
        FieldPanel("external_page"),
        FieldPanel("button_text"),
        FieldPanel("service_image")

    ]

    def clean(self):
        super().clean()
        if self.internal_page and self.external_page:
            raise ValidationError({
                'internal_page': ValidationError("Don't add both"),
                "external_page": ValidationError("Do not add both")
            })
        if not self.internal_page and not self.external_page:
            raise ValidationError({
                'internal_page': ValidationError("Enter a URL1"),
                "external_page": ValidationError("Enter a URL2")
            })
