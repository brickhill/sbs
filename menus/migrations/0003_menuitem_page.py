# Generated by Django 4.2.7 on 2024-01-30 22:07

from django.db import migrations
import django.db.models.deletion
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('menus', '0002_menuitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='menuitem',
            name='page',
            field=modelcluster.fields.ParentalKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='menu_items', to='menus.menu'),
            preserve_default=False,
        ),
    ]