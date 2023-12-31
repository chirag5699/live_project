# Generated by Django 4.2.2 on 2023-07-03 03:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('app_seller', '0005_delete_listing_data_delete_seller_data'),
    ]

    operations = [
        migrations.CreateModel(
            name='Seller_data',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstname', models.CharField(default='Anonymous', max_length=50)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('Mobile_No', models.CharField(default='Anonymous', max_length=50)),
                ('password', models.CharField(default='Anonymous', max_length=100)),
                ('propic', models.FileField(default='anonymous.jpg', upload_to='seller/')),
            ],
        ),
        migrations.CreateModel(
            name='Listing_data',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Listing_immage', models.FileField(default='Listing/abc.jpg', upload_to='Listing/')),
                ('P_id', models.CharField(max_length=100)),
                ('P_name', models.CharField(max_length=100)),
                ('P_Price', models.IntegerField()),
                ('P_Quntity', models.CharField(max_length=50)),
                ('P_Color', models.CharField(max_length=100)),
                ('P_fabric', models.CharField(max_length=50)),
                ('P_Tex_ammount', models.CharField(max_length=50)),
                ('P_Description', models.TextField(max_length=500)),
                ('seller_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_seller.seller_data')),
            ],
        ),
    ]
