# Generated by Django 3.1.3 on 2020-11-18 11:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0009_remove_listing_current_bid'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bid',
            options={'ordering': ['-bid_amount']},
        ),
    ]
