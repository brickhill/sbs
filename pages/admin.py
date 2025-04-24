from django.contrib import admin
from .models import Category, Tag, BlogPost
from django import forms


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
    list_display = ['title', 'author', 'updated']
    readonly_fields = ['created', 'updated']
    fields = ['title', 'body', 'synopsis', 'author', 'status',
              'start_time', 'end_time', 'categories', 'tags', 'created',
              'updated']
    exclude = []


admin.site.register(Tag)
admin.site.register(Category, CategoryAdmin)
admin.site.register(BlogPost, BLogPostAdmin)
