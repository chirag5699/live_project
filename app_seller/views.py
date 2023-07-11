
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render
from .models import *
import random 
import datetime
import time
from datetime import datetime
from django.contrib.auth.hashers import make_password,check_password
from django.shortcuts import redirect

# Create your views here.

def login_required_custom(view_func):
    def wrapper(request, *args, **kwargs):
        try:
            request.session["email"]
        except:
            return redirect('Login')  # Replace 'login' with the URL name of your login page
        return view_func(request, *args, **kwargs)
    return wrapper


 
def seller_index(request):
     return render(request,'seller_index.html')
 
def seller_Register(request):
    if request.method == 'POST':
        global user_otp,temp,start_time
        if request.POST['password']==request.POST['Cpassword']:
            temp={
                "firstname":request.POST['firstname'],
                "email":request.POST['email'],
                "Mobile_No":request.POST['Mobile_No'],
                "password":request.POST['password'] 
            }
            user_otp=random.randint(1000,9999)
            start_time= datetime.now().time()
            subject = 'OTP VERIFICATIONS PROCESS E-SHOPPER'
            message = f'Verification code Please use the verification code below to sign in. \n\n {user_otp}\n\nfrom django.utils.translation import ungettextIf you didn''t request this,\n you can ignore this email.\n\n Thanks,\n The E-shopper team '
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [request.POST['email']]
            send_mail(subject, message, email_from, recipient_list )
            return render (request,'seller_otp.html',{'msg':'otp valid in 30 secound'})          
        else:
            return render(request,'seller_register.html',{'msg':'password and cpassword are not match'})
    else:
        return render(request,'seller_register.html')
     
     
     
def seller_otp(request):
    if request.method == 'POST':
        if user_otp==int(request.POST['otp']):
            end_time = datetime.now().time()
            time_diff = datetime.combine(datetime.today(),end_time) - datetime.combine(datetime.today(), start_time)   
            second_diff= time_diff.total_seconds() 
            if second_diff < 30:
                Seller_data.objects.create(
                    firstname=temp["firstname"],
                    email=temp["email"],
                    Mobile_No=temp["Mobile_No"],
                    password=make_password(temp["password"])
            )
                return render(request,'seller_Register.html',{'msg':'Register Successfull'})
            else:
                return render (request,'seller_Register.html',{'msg':'otp Enter in time out','msg2':'otp velid in 40 secound'})           
        else:
            return render (request,'seller_Register.html',{'msg':'your otp is not match '})
    else:
        return render(request,"seller_Register.html") 
    

def seller_Login(request):
    if request.method == 'POST':
        try:
            Seller_indata=Seller_data.objects.get(email=request.POST["email"])
            # Seller_data=Seller_data.objects.get(email=request.POST['email'])
            check_password(request.POST["password"],Seller_indata.password)and(Seller_indata.firstname==request.POST["firstname"])
            request.session["email"] = request.POST["email"]
            return render(request,'seller_shop.html',{'msg':Seller_indata.firstname,'msg2':Seller_indata.email,'Seller_indata':Seller_indata})  
     
        except:
            return render(request,'seller_Login.html',{'msg':'User not exist plese registration'})      
    else:
        return render(request,'seller_Login.html')   
    
    
# @login_required_custom    
def seller_Logout(request):
    del request.session["email"] 
    return render(request,'seller_Login.html',{'msg':'seller user Logout successfully'})  

# @login_required_custom
def seller_profile(request):
    if request.method == 'POST': 
        Seller_indata=Seller_data.objects.get(email=request.session['email'])
        try:
            profile_im=request.FILES["propic"]
        except:
            profile_im=Seller_indata.propic
        if request.POST["new_password"]:
            if check_password(request.POST['Old_password'],Seller_indata.password):
                if request.POST['new_password'] == request.POST['Canform_new_Password']:
                    Seller_indata.password=make_password(request.POST['new_password'])
                    Seller_indata.firstname=request.POST['firstname']
                    Seller_indata.propic=profile_im
                    Seller_indata.save() 
                    return render (request,'seller_profile.html',{'Seller_indata':Seller_indata,'msg':'Profile update is succeccfully'})   
                else:
                     return render (request,'seller_profile.html',{'Seller_indata':Seller_indata,'msg':'new_password and Canform_new_Password are not match '})
            else:
                return render (request,'seller_profile.html',{'Seller_indata':Seller_indata,'msg':'Old password are not match'})
        else:
            Seller_indata.firstname=request.POST['firstname']
            Seller_indata.propic=profile_im       
            Seller_indata.save()
            return render (request,'seller_profile.html',{'Seller_indata':Seller_indata,'msg':'Update is succeccfully'})
    else:
        Seller_indata=Seller_data.objects.get(email=request.session['email'])
        return render (request,'seller_profile.html',{'Seller_indata':Seller_indata})
    
    
# @login_required_custom    
def seller_listing(request):
    Seller_indata=Seller_data.objects.get(email=request.session['email'])
    if request.method == 'POST':
        Selected_choice=request.POST.getlist('P_size')
        Selected_choice_str=",".join(Selected_choice) 
        Selected_color=request.POST.getlist('P_size')
        Selected_color_str=",".join(Selected_color) 
        try:
            request.FILES['Listing_immage'] 
            Listing_data.objects.create(
                Listing_immage=request.FILES['Listing_immage'],
                P_name=request.POST['P_name'],
                P_Price=request.POST['P_Price'],
                P_sellprice=request.POST['P_sellprice'], 
                P_Quntity=request.POST['P_Quntity'],
                P_Color=Selected_color_str,
                P_Description=request.POST['P_Description'],
                P_size=Selected_choice_str,
                seller_id=Seller_indata       
            )
        except:
            Listing_data.objects.create(
                P_name=request.POST['P_name'],
                P_Price=request.POST['P_Price'],
                P_sellprice=request.POST['P_sellprice'], 
                P_Quntity=request.POST['P_Quntity'],
                P_Color=Selected_color_str,
                P_Description=request.POST['P_Description'],
                P_size=Selected_choice_str,
                seller_id=Seller_indata 
            )             
        return render(request,'seller_listing.html',{'msg':'Data add is successfully...','Seller_indata':Seller_indata})  
    else:
        size=Listing_data.Size
        color=Listing_data.Color
        return render (request,'seller_listing.html',{'Seller_indata':Seller_indata,"size":size,"color":color})

# @login_required_custom
def seller_listing_Table(request):
    Seller_indata=Seller_data.objects.get(email=request.session['email'])
    seller_all_data=Listing_data.objects.filter(seller_id=Seller_indata)
    return render(request,'seller_listing_Table.html',{'seller_all_data':seller_all_data,"Seller_indata":Seller_indata,'msg':' Listing Update is successfully' })

# @login_required_custom
def Seller_update_listing(request,ck):
    
    Seller_indata=Seller_data.objects.get(email=request.session['email'])
    if request.method == 'POST':
        Selected_choice=request.POST.getlist('P_size')
        Selected_choice_str=",".join(Selected_choice)
        
        Selected_choice_color=request.POST.getlist('P_Color')
        Selected_choice_color_str=",".join( Selected_choice_color)
        one_data=Listing_data.objects.get(id=ck)
        try:
             listing_im=request.FILES['Listing_immage'] 
        except:
            listing_im=one_data.Listing_immage
           
        one_data.Listing_immage=listing_im
        one_data.P_name=request.POST['P_name']
        one_data.P_Price=request.POST['P_Price']
        one_data.P_sellprice=request.POST['P_sellprice'] 
        one_data.P_Quntity=request.POST['P_Quntity'] 
        one_data.P_Color=Selected_choice_color_str 
        one_data.P_size=Selected_choice_str
        one_data.P_Description=request.POST['P_Description']
        one_data.save() 
        return seller_listing_Table(request)  
    else:
        size=Listing_data.Size
        color=Listing_data.Color
        one_data=Listing_data.objects.get(id=ck)
        list_size=one_data.P_size.split(",")
        list_color=one_data.P_Color.split(",")
        return render(request,'Seller_update_listing.html',{'Seller_indata':Seller_indata,"one_data":one_data,"size":size,"list_size":list_size,'color':color,'list_color':list_color}) 
    
    
# @login_required_custom    
def Seller_delete_listing(request,ck):
    one_data=Listing_data.objects.get(id=ck)
    Seller_indata=Seller_data.objects.get(email=request.session['email'])
    seller_all_data=Listing_data.objects.filter(seller_id=Seller_indata)
    one_data.delete()
    return seller_listing_Table(request)        
            
        
        
