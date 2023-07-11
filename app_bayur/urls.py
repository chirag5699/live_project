from django.urls import path
from app_bayur import views

urlpatterns = [
   
   path('', views.index, name='index'),
   path('Register/',views.Register, name='Register'),
   path('otp/', views.otp, name='otp'),
   # path('Recent/', views.Recent, name='Recent'),
   path('Login/', views.Login, name='Login'),
   path('Logout/',views.Logout, name='Logout'),
   path('profile/',views.profile, name='profile'),
   path('shop/',views.shop, name='shop'),
   path('singal_product/<int:ck>',views.singal_product, name='singal_product'),
   path('Add_To_Cart/<int:ck>',views.Add_To_Cart, name='Add_To_Cart'),
   path('Show_cart',views.Show_cart, name='Show_cart'),
   path('Error',views.Error, name='Error'),
   path('Remove_cart/<int:ck>',views.Remove_cart, name='Remove_cart'),
   path('Update_cart/',views.Update_cart, name='Update_cart'),
   path('continue_shoping/',views.continue_shoping, name='continue_shoping'),
   path('checkout/',views.checkout, name='checkout'),
   path('paymenthandler/', views.paymenthandler, name='paymenthandler'),

   


   
]
