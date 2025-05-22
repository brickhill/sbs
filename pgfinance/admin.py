from django.contrib import admin
from .models import Country


class CountryAdmin(admin.ModelAdmin):
    date_hierarchy = 'updated'
    actions = []
    list_filter = ['created', 'updated']
    list_display = ['id', 'name', 'created', 'updated']
    readonly_fields = ['created', 'updated']
    fields = ['name', 'created', 'updated']
    exclude = []


admin.site.register(Country, CountryAdmin)
