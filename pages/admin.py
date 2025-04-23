from django.contrib import admin

from .models import Category

class CategoryAdmin(admin.ModelAdmin):
    date_hierarchy = 'updated'
    actions = []
    list_display = ['title', 'lft', 'rgt', 'level', 'created', 'updated']
    readonly_fields = ['created', 'updated']
    fields = ['title', 'description', 'lft', 'rgt', 'level', 'created', 'updated']
    exclude = []

admin.site.register(Category, CategoryAdmin)