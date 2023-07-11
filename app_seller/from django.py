# from django.db import models

# # Create your models here.



# # class Seller_data(models.Model,null=True):
# #     firstname=models.CharField(max_length=50,default=50)
# #     email=models.EmailField(unique=True,default=50)
# #     Mobile_No=models.CharField(max_length=50,default=50)
# #     password=models.CharField(max_length=100,default=50)
# #     propic=models.FileField(upload_to='seller/',default="anonymous.jpg")

# #     def __init__(self,args,*kwargs):
# #        super().__init_(args,*kwargs)
            
# #     def __str__(self):
# #         return self.firstname

# class Seller_data(models.Model):
#     firstname = models.CharField(max_length=50, default='Anonymous')
#     email = models.EmailField(unique=True)
#     Mobile_No = models.CharField(max_length=50, default='Anonymous')
#     password = models.CharField(max_length=100, default='Anonymous')
#     propic = models.FileField(upload_to='seller/', default="anonymous.jpg")
    
#     # def __init__(self, *args, **kwargs):
#     #     super()._init_(*args, **kwargs)

#     # def _str_(self):
#     #     return self.firstname

        
    
# class Listing_data(models.Model,null=True):
#     # def __init_subclass__(cls, *args, **kwargs):
#     #     super().__init_subclass__(*args, **kwargs)
    
#     Listing_immage=models.FileField(upload_to='Listing/',default="Listing/abc.jpg",)
#     P_id=models.CharField(max_length=100)
#     P_name=models.CharField(max_length=100)
#     P_Price=models.IntegerField()
#     P_Quntity=models.CharField(max_length=50)
#     P_Color=models.CharField(max_length=100)
#     P_fabric=models.CharField(max_length=50)
#     P_Tex_ammount=models.CharField(max_length=50)
#     P_Description=models.TextField(max_length=500)
#     seller_id=models.ForeignKey(Seller_data,on_delete=models.CASCADE)











# -------------------------------------------------------------------



from django.db import models


# # Create your models here.


# class Seller_data(models.Model):
#     firstname = models.CharField(max_length=50)
#     email = models.EmailField(unique=True)
#     Mobile_No = models.CharField(max_length=50)
#     password = models.CharField(max_length=100)
#     propic = models.FileField(upload_to='seller/', default="anonymous.jpg")
    
#     def __str__(self):
#         return self.firstname 
    
        
# class Listing_data(models.Model):
    
#     Listing_immage=models.FileField(upload_to='Listing/',default="Listing/abc.jpg")
#     P_name=models.CharField(max_length=100)
#     P_Price=models.CharField(max_length=100)
#     P_sellprice=models.CharField(max_length=100)
#     P_Quntity=models.CharField( max_length=50)
    
#     Color = [('Black', 'Black'),('White', 'White'),('Red', 'Red'),('Blue', 'Blue'),('Green', 'Green')]
#     P_Color=models.CharField(choices=Color,max_length=100, blank=True )
    
#     Size = [('XS', 'XS'),('S', 'S'),('M', 'M'),('L', 'L'),('XL', 'XL')]
#     P_size =models.CharField(choices=Size,max_length=100, blank=True )
#     P_Description=models.CharField(max_length=500)
#     seller_id=models.ForeignKey(Seller_data , on_delete=models.CASCADE)
     
    
#     def __str__(self):
#         return self.P_name 
