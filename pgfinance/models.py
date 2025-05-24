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
    EURO = "EUR"
    USDOLLAR = "USD"
    STERLING = "GBP"
    CURRENCY_CHOICES = ((EURO, "Euro"),
                        (USDOLLAR, "US Dollar"),
                        (STERLING, "Sterling"))
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
    symbol_yahoo = models.CharField(max_length=8, blank=True, null=True, help_text="Yahoo symbol")
    symbol_google = models.CharField(max_length=8, blank=True, null=True, help_text="Google symbol")
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES)
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
