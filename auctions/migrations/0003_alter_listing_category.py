# Generated by Django 4.2.7 on 2024-01-12 05:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_delete_pos_listing_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='category',
            field=models.CharField(choices=[('NC', 'No category'), ('C1', 'Category 1'), ('C2', 'Category 2'), ('C3', 'Category 3')], default='NC', max_length=24),
        ),
    ]
