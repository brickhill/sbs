from django.contrib import admin
from .models import Country, Index, Industry, Company


class CountryAdmin(admin.ModelAdmin):
    date_hierarchy = 'updated'
    actions = []
    list_filter = ['name', 'created', 'updated']
    list_display = ['id', 'name', 'created', 'updated']
    readonly_fields = ['created', 'updated']
    fields = ['name', 'created', 'updated']
    exclude = []


class IndexAdmin(admin.ModelAdmin):
    date_hierarchy = 'updated'
    actions = []
    list_filter = ['name', 'created', 'updated']
    list_display = ['id', 'name', 'created', 'updated']
    readonly_fields = ['created', 'updated']
    fields = ['name', 'created', 'updated']
    exclude = []


class IndustryAdmin(admin.ModelAdmin):
    date_hierarchy = 'updated'
    actions = []
    list_filter = ['name', 'created', 'updated']
    list_display = ['id', 'name', 'created', 'updated']
    readonly_fields = ['created', 'updated']
    fields = ['name', 'created', 'updated']
    exclude = []

class CompanyAdmin(admin.ModelAdmin):
    date_hierarchy = 'prices_updated'
    actions = []
    list_filter = ['country', 'index', 'industry']
    list_display = ['symbol', 'name', 'prices_updated']
    readonly_fields = ['created', 'updated']


admin.site.register(Country, CountryAdmin)
admin.site.register(Index, IndexAdmin)
admin.site.register(Industry, IndustryAdmin)
admin.site.register(Company, CompanyAdmin)
