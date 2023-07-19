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
    
class checkout_detail(models.Model):
    firstname=models.CharField(max_length=50)  
    lastname=models.CharField(max_length=50)  
    email=models.EmailField(max_length=20)
    mobile_no=models.IntegerField(default=0)
    address1=models.CharField(max_length=1000)
    address2=models.CharField(max_length=1000)
    City=models.CharField(max_length=50)
    State=models.CharField(max_length=50)  
    Country=models.CharField(max_length=50)
    ZIPCode=models.IntegerField(default=0)
    bayer_detials=models.ForeignKey(Add_user,on_delete=models.CASCADE,null=True)
    order_id=models.CharField(max_length=50)
    
    def __str__(self):
        return self.firstname
    
class Cart(models.Model):
    Product_id=models.ForeignKey(Listing_data,on_delete=models.CASCADE)
    Details_id=models.ForeignKey(checkout_detail,on_delete=models.CASCADE,null=True)
    Bayer_id=models.ForeignKey(Add_user,on_delete=models.CASCADE) 
    Quntity=models.IntegerField(default=0)
    product_color=models.CharField(max_length=50)
    product_size=models.CharField(max_length=50)
    total=models.IntegerField(default=0)
    status=models.BooleanField(default=True)
    
    
      
    def __str__(self):
        return str(self.Product_id)
    