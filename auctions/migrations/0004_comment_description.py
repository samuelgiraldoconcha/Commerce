# Generated by Django 4.2.7 on 2024-01-12 07:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_alter_listing_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='description',
            field=models.CharField(default=None, max_length=200),
        ),
    ]
