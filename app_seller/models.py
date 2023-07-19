from django.db import models


# Create your models here.


class Seller_data(models.Model):
    firstname = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    Mobile_No = models.CharField(max_length=50)
    password = models.CharField(max_length=100)
    propic = models.FileField(upload_to='seller/', default="anonymous.jpg")
    
    def __str__(self):
        return self.firstname 
    
        
class Listing_data(models.Model):
    
    Listing_immage=models.FileField(upload_to='Listing/',default="Listing/abc.jpg")
    P_name=models.CharField(max_length=100)
    P_Price=models.IntegerField(default=0)
    P_sellprice=models.CharField(max_length=100)
    P_Quntity=models.IntegerField(default=0)
    
    Color = [('Black', 'Black'),('White', 'White'),('Red', 'Red'),('Blue', 'Blue'),('Green', 'Green')]
    P_Color=models.CharField(choices=Color,max_length=100, blank=True )
    
    Size = [('XS', 'XS'),('S', 'S'),('M', 'M'),('L', 'L'),('XL', 'XL')]
    P_size =models.CharField(choices=Size,max_length=100, blank=True )
    P_Description=models.CharField(max_length=500)
    P_Categary=models.CharField(max_length=50,null=True)
    seller_id=models.ForeignKey(Seller_data , on_delete=models.CASCADE,null=True)
    
    def __str__(self):
        return self.P_name 
