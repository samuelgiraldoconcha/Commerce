# Generated by Django 4.2.7 on 2024-01-12 05:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='POS',
        ),
        migrations.AddField(
            model_name='listing',
            name='category',
            field=models.CharField(choices=[('NC', 'No category')], default='NC', max_length=24),
        ),
    ]
