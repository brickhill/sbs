from django.db import models
from wagtail.search import index
from wagtail.snippets.models import register_snippet
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from wagtail.models import Page, Orderable
from wagtail.fields import StreamField
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, InlinePanel, \
    MultiFieldPanel, PageChooserPanel
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase
from streams.models import TitleBlock, CardsBlock


class HomePage(Page):

    lead_text = models.CharField(
        max_length=500,
        help_text='Add some Lead text',
        blank=True
    )

    body = RichTextField(blank=True)

    button = models.ForeignKey('wagtailcore.Page',
                               blank=True,
                               null=True,
                               related_name='+',
                               help_text='Select page',
                               on_delete=models.SET_NULL
                               )

    button_text = models.CharField(
        max_length=50,
        help_text='Button Text',
        default='Read more',
        blank=False,
        null=False
    )

    banner_background_image = models.ForeignKey('wagtailimages.Image',
                                                blank=True,
                                                null=True,
                                                related_name='+',
                                                on_delete=models.SET_NULL
                                                )
    body_stream = StreamField([
        ("title", TitleBlock()),
        ("cards", CardsBlock())
    ], null=True, blank=True, use_json_field=True)
    content_panels = Page.content_panels + [
        FieldPanel("lead_text"),
        FieldPanel("body"),
        PageChooserPanel("button"),
        FieldPanel("button_text"),
        FieldPanel("banner_background_image"),
        FieldPanel("body_stream")
    ]
