from django.contrib import admin
from .models import Category, Tag, BlogPost, WebPage, CodeSnippet, BlogSeries, BlogPostSeries
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
    list_filter = ['level', 'created', 'updated']
    list_display = ['title', 'lft', 'rgt', 'level', 'created', 'updated']
    readonly_fields = ['created', 'updated']
    # fields = ['title', 'description', 'lft', 'rgt',
    #           'level', 'created', 'updated']
    exclude = []
    # form = CustomCategoryAdminForm

    # def save_model(self, request, obj, form, change):
        # Handle the extra field here if needed
        # parent = form.cleaned_data.get('parent')
        # TODO How do I display a list of categories to pick a parent?
        # obj.lft = parent
        # Perform any actions with extra_field_value
        # super().save_model(request, obj, form, change)


class BlogSeriesAdmin(admin.ModelAdmin):
    fields = ['title']
    list_filter = ['blogpost', 'created', 'updated']
    readonly_fields = ['created', 'updated']


class BlogPostSeriesAdmin(admin.ModelAdmin):
    fields = ['blogpost', 'series', 'priority']
    list_display = ['blogpost', 'series', 'priority']
    list_filter = ['series', 'blogpost']


class BlogPostAdmin(admin.ModelAdmin):
    date_hierarchy = 'updated'
    
    actions = []
    readonly_fields = ['created', 'updated']

    def image_tag(self, obj):
        if obj.feature_image:
            print(obj.feature_image)
            return format_html(f'<img src="{format(obj.feature_image.url)}"'
                               + ' style="max-width:200px;'
                               + ' max-height:200px"/>'
                               )
        else:
            return "<none>"

    list_display = ['title', 'status', 'image_tag', 'author', 'updated']
    fields = ['title', 'body', 'synopsis', 'author', 'status',
              'start_time', 'end_time', 'categories', 'tags', 'feature_image',
              'created', 'updated']
    list_filter = ['author', 'status', 'created', 'updated']
    exclude = []


class WebPageAdmin(admin.ModelAdmin):
    # TODO Special types (e.g. Privacy) must only have maximum
    date_hierarchy = 'updated'
    actions = []
    list_display = ['title', 'type', 'status', 'level', 'priority', 'author',
                    'updated', 'parent']
    readonly_fields = ['created', 'updated']
    fields = ['title', 'body', 'type', 'synopsis', 'level', 'priority',
              'author', 'status', 'created', 'updated', 'parent',
              'feature_image']
    exclude = []


class CodeSnippetAdmin(admin.ModelAdmin):
    date_hierarchy = 'updated'
    list_display = ['id', 'title']
    fields = ['title', 'snippet']
    readonly_fields = ['created', 'updated']


admin.site.register(Tag)
admin.site.register(CodeSnippet, CodeSnippetAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(BlogPost, BlogPostAdmin)
admin.site.register(BlogSeries, BlogSeriesAdmin)
admin.site.register(BlogPostSeries, BlogPostSeriesAdmin)
admin.site.register(WebPage, WebPageAdmin)
