
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render
from .models import *
import random 
import datetime
import time
from datetime import datetime
from django.contrib.auth.hashers import make_password,check_password
from app_seller.models import *
from django.db.models import Q
from django.shortcuts import redirect

def login_required_custom(view_func):     # define Decorators
    def wrapper(request, *args, **kwargs):
        try:
            request.session["email"]
        except:
            return redirect("Error")      # Replace 'login' with the URL name of your login page
        return view_func(request, *args, **kwargs)
    return wrapper 

def Error(request):
    return render (request,'404_Errer.html',{'msg':'Pleace Login first'})


def index(request):
    return render (request ,'index.html')


def Register(request):
    if request.method == 'POST':
        if request.POST['password'] == request.POST['Cpassword']:    # otp sending
            global user_otp, start_time,temp
            temp={
                "firstname":request.POST['firstname'],
                "email":request.POST['email'],
                "Mobile_No":request.POST['Mobile_No'],
                "password":request.POST['password'] 
            }
                # list1=['c','h','i','r','a','g' ,'5','6','9','9']
                # a=random.choices(list1,k=5)
                # user_otp="".join(a)
            user_otp=random.randint(10000,99999)
            start_time= datetime.now().time()
            subject = 'OTP VERIFICATIONS PROCESS E-SHOPPER'
            message = f'Verification code Please use the verification code below to sign in. \n\n {user_otp}\n\nfrom django.utils.translation import ungettextIf you didn''t request this,\n you can ignore this email.\n\n Thanks,\n The E-shopper team '
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [request.POST['email']]
            send_mail(subject, message, email_from, recipient_list )
            return render (request,'otp.html',{'msg':'otp valid in 30 secound'})       
        else:
            return render (request,'Register.html',{'msg':'Password & Canfirm password do not match'})                
    else:
        return render (request,'Register.html')
       

def otp(request):
    if request.method == "POST":
        if user_otp==int(request.POST["otp"]):
            end_time = datetime.now().time()
            time_diff = datetime.combine(datetime.today(),end_time) - datetime.combine(datetime.today(), start_time)   
            second_diff= time_diff.total_seconds() 
            if second_diff < 120:
                Add_user.objects.create(
                    firstname=temp["firstname"],
                    email=temp["email"],
                    Mobile_No=temp["Mobile_No"],
                    password=make_password(temp["password"])
            )
                return render(request,'Register.html',{'msg':'Register Successfull'})
            else:
                return render (request,'Register.html',{'msg':'otp Enter in time out','msg2':'otp velid in 120 secound'})           
        else:
            return render (request,'Register.html',{'msg':'otp is not match'})  
    else:
        return render(request,"Register.html")    
            

# def Recent(request):
#     subject = 'OTP VERIFICATIONS PROCESS E-SHOPPER'
#     message = f'Thank for chooising us your otp is {user_otp}'
#     email_from = settings.EMAIL_HOST_USER
#     recipient_list = [request.POST['email']]
#     send_mail(subject, message, email_from, recipient_list )
#     return render (request,'otp.html',{'msg':'Recent otp'})
     



def Login(request):
    if request.method == 'POST':
        
        try:   
            user_data=Add_user.objects.get(email=request.POST["email"])         
            if check_password(request.POST["password"],user_data.password)and(user_data.firstname==request.POST["firstname"]):
                request.session["email"] = request.POST["email"]
                all_product=Listing_data.objects.all()
                return render(request,'shop.html',{'msg':user_data.firstname,'msg2':user_data.email,"all_product":all_product,"user_data":user_data})
            else:
                return render(request,'Login.html',{'msg':'sorry your Information  not match TRY AGEAN '})
        except:
            return render(request,'Login.html',{'msg':'User not exist plese registration'})
    else:
        return render(request,'Login.html')
            
@login_required_custom                    
def Logout(request):
    del request.session["email"]
    return render (request,'Login.html',{'msg':'User Logout successfully '})

@login_required_custom    # use  Decorators
def profile(request):
    user_data=Add_user.objects.get(email=request.session["email"])
    if request.method == 'POST': 
        profile_data=Add_user.objects.get(email=request.session['email'])
        try:
            profile_im=request.FILES["propic"]
        except:
            profile_im=profile_data.propic
        if request.POST["new_password"]:
            if check_password(request.POST['Old_password'],profile_data.password):
                if request.POST['new_password'] == request.POST['Canform_new_Password']:
                    profile_data.password=make_password(request.POST['new_password'])
                    profile_data.firstname=request.POST['firstname']
                    profile_data.propic=profile_im
                    profile_data.save() 
                    return render (request,'profile.html',{'profile_data':profile_data,"user_data":user_data,'msg':'Profile update is succeccfully'})   
                else:
                     return render (request,'profile.html',{'profile_data':profile_data,"user_data":user_data,'msg':'new_password and Canform_new_Password are not match '})
            else:
                return render (request,'profile.html',{'profile_data':profile_data,"user_data":user_data,'msg':'Old password are not match'})
        else:
            profile_data.firstname=request.POST['firstname']
            profile_data.propic=profile_im       
            profile_data.save()
            return render (request,'profile.html',{'profile_data':profile_data,"user_data":user_data,'msg':'Update is succeccfully'})
    else:
        profile_data=Add_user.objects.get(email=request.session['email'])
        return render (request,'profile.html',{'profile_data':profile_data,"user_data":user_data})
    
@login_required_custom   # use  Decorators
def shop(request):
    user_data=Add_user.objects.get(email=request.session["email"])
    all_product=Listing_data.objects.all()
    return render (request,'shop.html',{"all_product":all_product ,'user_data': user_data})

@login_required_custom   # use  Decorators

def singal_product(request,ck):
    user_data=Add_user.objects.get(email=request.session["email"])
    one_product=Listing_data.objects.get(id=ck)
    return render(request,'Shop_Detail.html',{"one_product":one_product,'user_data':user_data,"sizes":one_product.P_size.split(","),"colors":one_product.P_Color.split(",")})

@login_required_custom   # use  Decorators

def Add_To_Cart(request,ck):
    
    Current_Login=Add_user.objects.get(email=request.session['email'])
    Product=Listing_data.objects.get(id=ck)
    if request.method == 'POST':
        try:
            allredy_data=Cart.objects.get(Q(Product_id=ck) & Q(Bayer_id=Current_Login.id))
            allredy_data.Quntity+=1
            allredy_data.total=allredy_data.Quntity*allredy_data.Product_id.P_Price
            allredy_data.save()
            return Show_cart(request)   
        except:
            Product=Listing_data.objects.get(id=ck)
            Cart.objects.create(
                Product_id=Product,
                Bayer_id=Current_Login,
                Quntity=1,
                total=Product.P_Price,
                product_color=request.POST["color"],
                product_size=request.POST['size'],
        )
            return Show_cart(request)
    else:
            return render (request,"cart.html")
        

@login_required_custom   # use  Decorators
def Show_cart(request):
    user_data=Add_user.objects.get(email=request.session["email"])
    Current_Login=Add_user.objects.get(email=request.session["email"])
    all_cart=Cart.objects.filter(Bayer_id=Current_Login.id)
    total_amount=0
    for i in all_cart:
        total_amount=total_amount+i.total
        gst_amount=(total_amount*10)/100
        final_amount=total_amount+gst_amount   
    return render (request,'cart.html',{'all_cart':all_cart,'user_data': user_data,'total_amount':total_amount,'gst_amount':gst_amount,'final_amount':final_amount})
  

def Remove_cart(request,ck):
    Cart_data=Cart.objects.get(id=ck)
    Cart_data.delete()
    return Show_cart(request)


def Update_cart(request):
    if request.method == 'POST':
        list_data=request.POST.getlist("UQuntity")   # quntity fild name value
        all_cart=Cart.objects.all() 
        for i,j in zip(all_cart,list_data):
            i.Quntity=j
            i.total=int(j)*i.Product_id.P_Price
            i.save()
        return Show_cart(request)
    else:
        return Show_cart(request)

    
def continue_shoping(request):
    return shop(request)


@login_required_custom                    
def checkout(request):
    user_data=Add_user.objects.get(email=request.session["email"])
    Current_Login=Add_user.objects.get(email=request.session["email"])
    all_cart=Cart.objects.filter(Bayer_id=Current_Login.id)
    total_amount=0
    for i in all_cart:
        total_amount=total_amount+i.total
        Shipping_amount=(total_amount*5)/100
        final_amount=total_amount+Shipping_amount   
    return render (request,'checkout.html',{'final_amount':final_amount,'all_cart':all_cart,'Shipping_amount':Shipping_amount,'total_amount':total_amount})





from django.shortcuts import render
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest


# authorize razorpay client with API Keys.
razorpay_client = razorpay.Client(
	auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

@csrf_exempt
def paymenthandler(request):

	# only accept POST request.
	if request.method == "POST":
		try:
		
			# get the required parameters from post request.
			payment_id = request.POST.get('razorpay_payment_id', '')
			razorpay_order_id = request.POST.get('razorpay_order_id', '')
			signature = request.POST.get('razorpay_signature', '')
			params_dict = {
				'razorpay_order_id': razorpay_order_id,
				'razorpay_payment_id': payment_id,
				'razorpay_signature': signature
			}

			# verify the payment signature.
			result = razorpay_client.utility.verify_payment_signature(
				params_dict)
			if result is not None:
				amount = 20000 # Rs. 200
				try:

					# capture the payemt
					razorpay_client.payment.capture(payment_id, amount)

					# render success page on successful caputre of payment
					return render(request, 'paymentsuccess.html')
				except:

					# if there is an error while capturing payment.
					return render(request, 'paymentfail.html')
			else:

				# if signature verification fails.
				return render(request, 'paymentfail.html')
		except:

			# if we don't find the required parameters in POST data
			return HttpResponseBadRequest()
	else:
	# if other than POST request is made.
		return HttpResponseBadRequest()



















    
    