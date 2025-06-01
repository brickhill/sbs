from django.contrib import admin
from .models import Country, Index, Industry, Company, Lookup, Price


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


class LookupInline(admin.TabularInline):
        model = Lookup


class CompanyAdmin(admin.ModelAdmin):
    date_hierarchy = 'prices_updated'
    actions = []
    list_filter = ['country', 'index', 'industry']
    list_display = ['symbol', 'name', 'prices_updated']
    readonly_fields = ['created', 'updated']
    inlines = [LookupInline,]


class LookupAdmin(admin.ModelAdmin):
    date_hierarchy = 'updated'
    actions = []
    list_filter = []
    list_display = ['company', 'symbol_yahoo', 'symbol_google', 'currency']
    readonly_fields = ['created', 'updated']

class PriceAdmin(admin.ModelAdmin):
    date_hierarchy = 'price_time'
    actions = []
    list_filter = ['company']
    list_display = ['price_time', 'company', 'open', 'high', 'low', 'close', 'volume']

admin.site.register(Country, CountryAdmin)
admin.site.register(Index, IndexAdmin)
admin.site.register(Industry, IndustryAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(Lookup, LookupAdmin)
admin.site.register(Price, PriceAdmin)