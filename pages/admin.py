from django.contrib import admin
from .models import Category, Tag, BlogPost, WebPage
from django import forms
from django.utils.html import format_html


class CustomCategoryAdminForm(forms.ModelForm):
    parent = forms.IntegerField()

    class Meta:
        model = Category
        fields = '__all__'


class CategoryAdmin(admin.ModelAdmin):
    date_hierarchy = 'updated'
    actions = []
    list_display = ['title', 'lft', 'rgt', 'level', 'created', 'updated']
    readonly_fields = ['created', 'updated']
    fields = ['title', 'description', 'lft', 'rgt', 'parent',
              'level', 'created', 'updated']
    exclude = []
    form = CustomCategoryAdminForm

    def save_model(self, request, obj, form, change):
        # Handle the extra field here if needed
        parent = form.cleaned_data.get('parent')
        # TODO How do I display a list of categories to pick a parent?
        print(f"PARENT{parent}")
        obj.lft = parent
        # Perform any actions with extra_field_value
        super().save_model(request, obj, form, change)


class BLogPostAdmin(admin.ModelAdmin):
    date_hierarchy = 'updated'
    actions = []
    readonly_fields = ['created', 'updated']
    def image_tag(self, obj):
        print(f"FEATURE:{obj.feature_image }")
        if obj.feature_image:
            print('A')
            print(obj.feature_image)
            return format_html('<img src="{}" style="max-width:200px; max-height:200px"/>'.format(obj.feature_image.url))
        else:
            print('B')
            return "<none>"

    list_display = ['title', 'image_tag', 'author', 'updated']
    fields = ['title', 'body', 'synopsis', 'author', 'status',
              'start_time', 'end_time', 'categories', 'tags', 'feature_image', 'created',
              'updated']
    exclude = []

class WebPageAdmin(admin.ModelAdmin):
    date_hierarchy = 'updated'
    actions = []
    list_display = ['title', 'level', 'priority', 'author', 'updated', 'parent']
    readonly_fields = ['created', 'updated']
    fields = ['title', 'body', 'synopsis', 'level', 'priority',
              'author', 'status', 'created', 'updated', 'parent', 'feature_image']
    exclude = []

admin.site.register(Tag)
admin.site.register(Category, CategoryAdmin)
admin.site.register(BlogPost, BLogPostAdmin)
admin.site.register(WebPage, WebPageAdmin)
