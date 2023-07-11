from django.db import models
from app_seller.models import *

# Create your models here.

class Add_user(models.Model):
    propic=models.FileField(upload_to="media/",default="anonymous.jpg")
    firstname=models.CharField(max_length=50)
    email=models.EmailField(unique=True)
    Mobile_No=models.CharField(max_length=50)
    password=models.CharField(max_length=100)
    
    def __str__(self):
        return self.firstname
    
    
class Cart(models.Model):
    Product_id=models.ForeignKey(Listing_data,on_delete=models.CASCADE)
    Bayer_id=models.ForeignKey(Add_user,on_delete=models.CASCADE) 
    Quntity=models.IntegerField(default=0)
    product_color=models.CharField(max_length=50)
    product_size=models.CharField(max_length=50)
    total=models.IntegerField(default=0)
      
    def __str__(self):
        return str(self.Product_id)
    
class checkout_detail(models.Model):
    firstname=models.CharField(max_length=50)  
    lastname=models.CharField(max_length=50)  
    email=models.EmailField(unique=True)
    mobile_no=models.IntegerField(default=0)
    address=models.CharField(max_length=1000)
    Country=models.CharField(max_length=50)
    bayer_id=models.ForeignKey(Add_user,on_delete=models.CASCADE)
    
    
    def __str__(self):
        return self.firstname