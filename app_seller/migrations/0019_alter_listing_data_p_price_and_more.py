# Generated by Django 4.2.2 on 2023-07-10 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_seller', '0018_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing_data',
            name='P_Price',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='listing_data',
            name='P_Quntity',
            field=models.IntegerField(default=0),
        ),
    ]
