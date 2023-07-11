# Generated by Django 4.2.2 on 2023-07-03 04:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_seller', '0006_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listing_data',
            name='P_Tex_ammount',
        ),
        migrations.AlterField(
            model_name='listing_data',
            name='P_Price',
            field=models.DecimalField(decimal_places=2, max_digits=8),
        ),
        migrations.AlterField(
            model_name='listing_data',
            name='P_Quntity',
            field=models.IntegerField(),
        ),
    ]
