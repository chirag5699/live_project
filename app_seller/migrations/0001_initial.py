# Generated by Django 4.2.2 on 2023-07-01 06:09

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Listing_data',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('P_id', models.CharField(max_length=100)),
                ('P_name', models.CharField(max_length=100)),
                ('P_Prise', models.CharField(max_length=50)),
                ('P_Quntity', models.CharField(max_length=50)),
                ('P_Color', models.CharField(max_length=100)),
                ('P_fabric', models.CharField(max_length=50)),
                ('P_Tex_ammount', models.CharField(max_length=50)),
                ('P_Description', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Seller_data',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstname', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('Mobile_No', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=100)),
                ('propic', models.FileField(default="'seller/abc.jpg", upload_to='seller/')),
            ],
        ),
    ]
