# Generated by Django 4.2.2 on 2023-07-10 09:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_bayur', '0002_cart'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='total',
            field=models.IntegerField(default=0),
        ),
    ]
