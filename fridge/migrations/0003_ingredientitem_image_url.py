# Generated by Django 5.2.1 on 2025-05-23 05:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fridge', '0002_ingredient'),
    ]

    operations = [
        migrations.AddField(
            model_name='ingredientitem',
            name='image_url',
            field=models.URLField(blank=True, null=True),
        ),
    ]
