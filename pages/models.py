from django.db import models
from django.contrib.auth.models import User


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
    PUBLISHED = "PUBISHED"
    STATUS_CHOICES = ((DRAFT, "Draft"), (PUBLISHED, "Published"))

    title = models.CharField(max_length=200, blank=False, null=False,
                             help_text="Post title", validators=[])
    body = models.TextField(max_length=20000, blank=False, null=False,
                            help_text="Blog body")
    synopsis = models.TextField(max_length=20000, blank=True, null=True,
                                help_text="Synopsis", validators=[])
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES,
                              blank=True, null=True, help_text='Status')
    start_time = models.DateTimeField(help_text="Optional Start time",
                                      db_index=True, blank=True,  null=True)
    end_time = models.DateTimeField(help_text="Optional end time",
                                    db_index=True, blank=True, null=True)
    categories = models.ManyToManyField(Category, help_text="Categories")
    tags = models.ManyToManyField(Tag, help_text="Tags", blank=True, null=True)
    feature_image = models.ImageField(blank=True, null=True)

    # TODO Why are tags (and categories) mandatory?
    # TODO Add comments (hierarchical)

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


class WebPage(models.Model):
    DRAFT = "DRAFT"
    PUBLISHED = "PUBISHED"
    STATUS_CHOICES = ((DRAFT, "Draft"), (PUBLISHED, "Published"))

    title = models.CharField(max_length=200, blank=False, null=False,
                             help_text="Post title", validators=[])
    body = models.TextField(max_length=20000, blank=False, null=False,
                            help_text="Blog body")
    synopsis = models.TextField(max_length=20000, blank=True, null=True,
                                help_text="Synopsis", validators=[])
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES,
                              blank=True, null=True, help_text='Status')
    parent = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True, default=None)
    feature_image = models.ImageField(upload_to="images/")
    lft = models.IntegerField(null=True, blank=True)
    rgt = models.IntegerField(null=True, blank=True)
    level = models.IntegerField(null=True, blank=True)


    def __str__(self):
        return self.title

    class Meta:
        # db_table_comment = "Blog post categories"
        verbose_name = "Web page"
        verbose_name_plural = "Web pages"
        ordering = ["title", "-updated"]
        indexes = [
            # models.Index(fields=['last', 'first'])
        ]
        unique_together = []
#############################

# TODO Comments: Who, Text, Post, LFT, RGT, Level
