
from django.urls import path
from app_seller import views

urlpatterns = [
    path('', views.seller_index, name='seller_index'),
    path('seller_Register/', views.seller_Register, name='seller_Register'),
    path('seller_otp/', views.seller_otp, name='seller_otp'),
    path('seller_Login/', views.seller_Login, name='seller_Login'),
    path('seller_Logout/', views.seller_Logout, name='seller_Logout'),
    path('seller_profile/', views.seller_profile, name='seller_profile'),
    path('seller_listing/', views.seller_listing, name='seller_listing'),
    path('seller_listing_Table/', views.seller_listing_Table, name='seller_listing_Table'),
    path('Seller_update_listing/<int:ck>/', views.Seller_update_listing, name='Seller_update_listing'),
    path('Seller_delete_listing/<int:ck>/', views.Seller_delete_listing, name='Seller_delete_listing'),
    path('seller_order/', views.seller_order, name='seller_order'),
    path('Accepte/<int:ck>', views.Accepte, name='Accepte'),
    path('Cencel/<int:ck>', views.Cencel, name='Cencel'),
    path('seller_Payment/', views.seller_Payment, name='seller_Payment'),
    
    
    
   
]
