from django.db import models
from wagtail.snippets.models import register_snippet


@register_snippet
class BlogPost(models.Model):
    title = models.CharField(max_length=250, blank=False, null=False,
                             help_text="Post Title")
    body = models.TextField(max_length=500, blank=False, null=False,
                            help_text="Post Body")
    extract = models.TextField(max_length=200, blank=True)
    '''
    status
    author
    from
    to
    '''

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Blog Post"
        verbose_name_plural = "Blog Posts"
