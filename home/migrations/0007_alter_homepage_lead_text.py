# Generated by Django 4.2.7 on 2023-12-05 22:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_alter_homepage_banner_background_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='homepage',
            name='lead_text',
            field=models.CharField(blank=True, help_text='Add some Lead text', max_length=500),
        ),
    ]
