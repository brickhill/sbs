from django.db import models


class Country(models.Model):
    name = models.CharField(max_length=30, blank=False, null=False, unique=True,
                            help_text="Country Name", validators=[])
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table_comment = "Countries"
        verbose_name = "Country"
        verbose_name_plural = "Blog Countries"
        ordering = ["name"]
        indexes = [
            # models.Index(fields=['last', 'first'])
        ]
        unique_together = []
