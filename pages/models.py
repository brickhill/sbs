from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    title = models.CharField(max_length=200, blank=False, null=False,
    help_text="Category Name", validators=[])
    # WRITE Describe options for Charfield
    # WRITE Describe validation options for Charfield.
    description = models.TextField(max_length=50, blank=True, null=True, 
    help_text="Description",validators=[])
    lft = models.IntegerField(blank=False, null=False, default=0, validators=[])
    rgt = models.IntegerField(blank=False, null=False, default=0,validators=[])
    level = models.IntegerField(default=1, blank=False, null=False, validators=[])
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
# Title
# Body
# Synopsis
# Created
# Updated
# Author (FK)
# Status (Draft/Published)
# Start Time
# End Time
# Categories (M/M)
# Comments (FK)
# Tags (M/M)
 
# Category
# Title
# Description
# LFT
# RGT
# Level
 
# Comments
# Who
# Text
# Post
# LFT
# RGT
# Level

# class Room(models.Model):
#     host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
#     topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
#     name = models.CharField(max_length=200)
#     description = models.TextField(null=True, blank=True)
#     participants = models.ManyToManyField(
#         User,
#         related_name="participants",
#         blank=True
#         )
#     updated = models.DateTimeField(auto_now=True)
#     created = models.DateTimeField(auto_now_add=True)

#     class Meta():
#         ordering = ['-updated', '-created']

#     def __str__(self):
#         return self.name


# class Message(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     room = models.ForeignKey(Room, on_delete=models.CASCADE)
#     body = models.TextField(null=True, blank=True)
#     updated = models.DateTimeField(auto_now=True)
#     created = models.DateTimeField(auto_now_add=True)

#     class Meta():
#         ordering = ['-updated', '-created']

#     def __str__(self):
#         return self.body[0:50]
