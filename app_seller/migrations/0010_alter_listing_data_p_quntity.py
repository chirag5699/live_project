# Generated by Django 4.2.2 on 2023-07-03 06:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_seller', '0009_alter_listing_data_p_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing_data',
            name='P_Quntity',
            field=models.CharField(max_length=50),
        ),
    ]