from django.db import models
from django.contrib.auth.models import User
# from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.db.models import Q
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.exceptions import ValidationError


class Category(models.Model):
    title = models.CharField(max_length=200, blank=False, null=False,
                             help_text="Category Name", validators=[])
    # WRITE Describe options for Charfield
    # WRITE Describe validation options for Charfield.
    description = models.TextField(max_length=50, blank=True, null=True,
                                   help_text="Description", validators=[])
    lft = models.IntegerField(blank=False, null=False, default=0,
                              validators=[])
    rgt = models.IntegerField(blank=False, null=False, default=0,
                              validators=[])
    level = models.IntegerField(default=1, blank=False, null=False,
                                validators=[])
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        # db_table_comment = "Blog post categories"
        verbose_name = "Blog Category"
        verbose_name_plural = "Blog Categories"
        ordering = ["title"]
        indexes = [
            # models.Index(fields=['last', 'first'])
        ]
        unique_together = []


class Tag(models.Model):
    title = models.CharField(max_length=200, blank=False, null=False,
                             help_text="Tag Name", validators=[])

    def __str__(self):
        return self.title


class BlogPost(models.Model):
    DRAFT = "DRAFT"
    PUBLISHED = "PUBLISHED"
    PAGE = "PAGE"
    TERMS = "T&C"
    PRIVACY = "PRIVACY"
    STATUS_CHOICES = ((DRAFT, "Draft"), (PUBLISHED, "Published"))
    TYPE_CHOICES = (
        (PAGE, "Page"), (TERMS, "Terms & Conditions"), (PRIVACY, "Privacy")
    )
    title = models.CharField(max_length=200, blank=False, null=False,
                             help_text="Post title", validators=[])
    body = RichTextUploadingField(max_length=20000, blank=False, null=False,
                                  help_text="Blog body")
    synopsis = models.TextField(max_length=20000, blank=True, null=True,
                                help_text="Synopsis", validators=[])
    updated = models.DateTimeField(auto_now=True)
    type = models.CharField(max_length=7,
                            blank=False,
                            null=False,
                            default=PAGE,
                            choices=TYPE_CHOICES)
    created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES,
                              blank=True, null=True, help_text='Status')
    start_time = models.DateTimeField(help_text="Optional Start time",
                                      db_index=True, blank=True,  null=True)
    end_time = models.DateTimeField(help_text="Optional end time",
                                    db_index=True, blank=True, null=True)
    categories = models.ManyToManyField(Category,
                                        help_text="Categories",
                                        blank=True)
    tags = models.ManyToManyField(Tag, help_text="Tags", blank=True)
    feature_image = models.ImageField(blank=True, null=True)

    # TODO Add comments (hierarchical)

    def get_class(self):
        return self.__class__.__name__
    
    def __str__(self):
        return self.title

    class Meta:
        # db_table_comment = "Blog post categories"
        verbose_name = "Blog Post"
        verbose_name_plural = "Blog Posts"
        ordering = ["title", "-updated"]
        indexes = [
            # models.Index(fields=['last', 'first'])
        ]
        unique_together = []


class BlogSeries(models.Model):

    title = models.CharField(max_length=200, blank=False, null=False,
                             help_text="Blog Series title", validators=[])
    blogpost = models.ManyToManyField(BlogPost, through="BlogPostSeries")

    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    description = RichTextUploadingField(
                                         max_length=20000,
                                         blank=True,
                                         null=True,
                                         help_text="Blog series description",
                                         validators=[])

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Blog Series"
        verbose_name_plural = "Blog Series"


class BlogPostSeries(models.Model):
    blogpost = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    series = models.ForeignKey(BlogSeries, on_delete=models.CASCADE)
    priority = models.IntegerField()

    
    def __str__(self):
        return self.blogpost.title

    class Meta:
        verbose_name = "Blog Post Series"
        verbose_name_plural = "Blog Post Series Entries"
        constraints = [
            models.UniqueConstraint(
                fields=["blogpost", "series"], name="unique_blogpost_series"
            ),
            models.UniqueConstraint(
                fields=["series", "priority"], name="unique_series_priority"
            )
        ]


@receiver(post_save, sender=BlogPostSeries)
def resequence_series(sender, instance, created, **kwargd):
    entries = BlogPostSeries.objects.filter(
                        series=instance.series).order_by("priority")
    priority = 0
    post_save.disconnect(resequence_series, sender=sender)

    for e in entries:
        priority -= 10
        e.priority = priority
        e.save()
    for e in entries:
        e.priority = e.priority * -1
        e.save()
    post_save.connect(resequence_series, sender=sender)


class WebPage(models.Model):
    DRAFT = "DRAFT"
    PUBLISHED = "PUBISHED"
    PAGE = "PAGE"
    TERMS = "T&C"
    PRIVACY = "PRIVACY"
    STATUS_CHOICES = ((DRAFT, "Draft"), (PUBLISHED, "Published"))
    TYPE_CHOICES = (
                    (PAGE, "Page"),
                    (TERMS, "Terms & Conditions"),
                    (PRIVACY, "Privacy Policy")
                   )
    title = models.CharField(max_length=200, blank=False, null=False,
                             help_text="Post title", validators=[])
    body = RichTextUploadingField(max_length=20000, null=False, blank=False,
                                  help_text="Blog body")
    synopsis = models.TextField(max_length=20000, blank=True, null=True,
                                help_text="Synopsis", validators=[])
    type = models.CharField(max_length=8,
                            null=False,
                            blank=False,
                            choices=TYPE_CHOICES,
                            default=PAGE,
                            help_text="Page Type")
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES,
                              blank=True, null=True, help_text='Status')
    parent = models.ForeignKey("self", on_delete=models.SET_NULL,
                               null=True, blank=True, default=None)
    feature_image = models.ImageField(upload_to="images/", null=True,
                                      blank=True)
    lft = models.IntegerField(null=True, blank=True)
    rgt = models.IntegerField(null=True, blank=True)
    level = models.IntegerField(default=1, null=True, blank=True)
    priority = models.IntegerField(default=1, null=True, blank=True)

    def __str__(self):
        return self.title
    
    def get_class(self):
        return self.__class__.__name__

    def clean(self, *args, **kwargs):
        super().clean()
        if self.type == self.TERMS or self.type == self.PRIVACY:
            result = WebPage.objects.filter(Q(type=self.type) & ~Q(id=self.id))
            if result:
                msg = f"Already type {self.type}"
                raise ValidationError({"type": msg})

    class Meta:
        # db_table_comment = "Blog post categories"
        verbose_name = "Web page"
        verbose_name_plural = "Web pages"
        ordering = ["title", "-updated"]
        indexes = [
            # models.Index(fields=['last', 'first'])
        ]
        unique_together = []


class CodeSnippet(models.Model):
    title = models.CharField(max_length=100, blank=False, null=False,
                             help_text="Snippet title")
    snippet = models.TextField(max_length=20000, blank=False, null=False,
                               help_text="Code Snippet")
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Code Snippet"
        ordering = ["title", "-updated"]
