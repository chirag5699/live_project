# Generated by Django 4.2.2 on 2023-07-13 05:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_bayur', '0005_checkout_detail_bayer_detials'),
    ]

    operations = [
        migrations.AddField(
            model_name='checkout_detail',
            name='order_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app_bayur.cart'),
        ),
    ]