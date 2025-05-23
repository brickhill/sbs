# Generated by Django 4.2.20 on 2025-04-24 20:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0003_tag_blogpost'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='blogpost',
            options={'ordering': ['title', '-updated'], 'verbose_name': 'Blog Post', 'verbose_name_plural': 'Blog Posts'},
        ),
        migrations.AlterField(
            model_name='blogpost',
            name='end_time',
            field=models.TimeField(blank=True, db_index=True, help_text='Optional end time', null=True),
        ),
        migrations.AlterField(
            model_name='blogpost',
            name='start_time',
            field=models.TimeField(blank=True, db_index=True, help_text='Optional Start time', null=True),
        ),
    ]
