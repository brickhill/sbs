from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator


class Country(models.Model):
    name = models.CharField(
                            max_length=30,
                            blank=False,
                            null=False,
                            unique=True,
                            help_text="Country Name",
                            validators=[]
                            )
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table_comment = "Countries"
        verbose_name = "Country"
        verbose_name_plural = "Countries"
        ordering = ["name"]
        indexes = [
            # models.Index(fields=['last', 'first'])
        ]
        unique_together = []


class Index(models.Model):
    name = models.CharField(
                            max_length=30,
                            blank=False,
                            null=False,
                            unique=True,
                            db_index=True,
                            help_text="Index Name",
                            validators=[])
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table_comment = "Indices"
        verbose_name = "Index"
        verbose_name_plural = "Indices"
        ordering = ["name"]
        unique_together = []


class Industry(models.Model):
    name = models.CharField(
                            max_length=30,
                            blank=False,
                            null=False,
                            unique=True,
                            help_text="Industry Name",
                            validators=[])
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table_comment = "Industry"
        verbose_name = "Industry"
        verbose_name_plural = "Industries"
        ordering = ["name"]
        unique_together = []


class Company(models.Model):

    ACTIVE = "A"
    INACTIVE = "I"
    STATUS_CHOICES = (
        (ACTIVE, "Active"),
        (INACTIVE, "Inactive")
    )
    name = models.CharField(
                            max_length=50,
                            blank=False,
                            null=False,
                            unique=True,
                            help_text="Company Name",
                            validators=[]
                            )
    symbol = models.CharField(
                              max_length=6,
                              blank=False,
                              null=False,
                              unique=True,
                              help_text="Company Symbol",
                              validators=[MinLengthValidator(2, "Too short"),
                                          MaxLengthValidator(6, "Too Long")
                                          ]
                              )
    country = models.ForeignKey(Country, on_delete=models.CASCADE, blank=False, null=False)
    index = models.ManyToManyField(Index, help_text="Indices", blank=False)
    industry = models.ManyToManyField(Industry, help_text="Industries", blank=False)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    prices_updated = models.DateTimeField(null=True, blank=True, help_text="Last Time Prices were updated")
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default=INACTIVE)

    class Meta:
        db_table_comment = "Companies"
        verbose_name = "Company"
        verbose_name_plural = "Companies"
        ordering = []
        indexes = []
        unique_together = []

    def __str__(self):
        return self.name

class Lookup(models.Model):
    EURO = "EUR"
    USDOLLAR = "USD"
    STERLING = "GBP"
    CURRENCY_CHOICES = ((EURO, "Euro"),
                        (USDOLLAR, "US Dollar"),
                        (STERLING, "Sterling"))
    company = models.ForeignKey(Company, on_delete=models.CASCADE, blank=False, null=False, db_index=True)
    symbol_yahoo = models.CharField(max_length=20, blank=False, null=False, help_text="Data source")
    symbol_google = models.CharField(max_length=20, blank=False, null=False, help_text="Google symbol")
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, null=False, blank=False, 
                                db_index=True, help_text="Currency Code")
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Data lookup'
        verbose_name_plural = 'Data lookups'
        ordering = ['company']
        indexes = []
        unique_together = [['company', 'symbol_yahoo', 'currency'],['company', 'symbol_google', 'currency']]
    
    def __str__(self):
        return self.symbol_yahoo

class Price(models.Model):
    
    DAILY = "D"
    FIVEMIN = "5"
    PERIOD_CHOICES = (
        (DAILY, "Daily"),
        (FIVEMIN, "5min")
    )
    price_time = models.DateTimeField(null=False, blank=False, help_text="Price Time")
    period = models.CharField(max_length=1, null=False, blank=False, default=DAILY, help_text="Period")
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=False, blank=False, db_index=True)
    lookup = models.ForeignKey(Lookup, on_delete=models.CASCADE, null=False,
                                blank=False, db_index=True)
    open = models.FloatField(null=True, blank=True)
    high = models.FloatField(null=True, blank=True)
    low = models.FloatField(null=True, blank=True)
    close = models.FloatField(null=True, blank=True)
    volume = models.BigIntegerField(null=True, blank=True)
    dividends = models.FloatField(null=True, blank=True)
    stock_splits = models.FloatField(null=True, blank=True)

    class Meta:
        verbose_name = 'Price'
        verbose_name_plural = 'Prices'
        ordering = ['company', 'price_time']
        # index_together = [('company', 'price_time')]
        # unique_together = [['company', 'period', 'price_time']]
    
    def __str__(self):
        return f"{self.company} ({self.price_time})"