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
from django.shortcuts import render
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
import requests

# ======================== Decorators ===================
def login_required_custom(view_func):     # define Decorators
    def wrapper(request, *args, **kwargs):
        try:
            request.session["email"]    # user email
        except:
            return redirect("Error")      # Replace 'login' with the URL name of your login page
        return view_func(request, *args, **kwargs)
    return wrapper 

# ======================== Errer fanction ===================
def Error(request):
    return render (request,'404_Errer.html',{'msg':'Pleace Login first'})


# ======================== Index fanction ===================
def index(request):
    try:
       
        all_num=Cart.objects.all().count()   # cart detail count
        all_num=Cart.objects.filter(Q(Bayer_id=user_data.id) & Q(status=True)).count()  # cart count 
        user_data=Add_user.objects.get(email=request.session["email"])   # session on
        return render (request,'index.html',{'msg':user_data.firstname,'msg2':user_data.email,'all_num':all_num,'user_data':user_data,'all_product':all_product}) #  {} ->   data Deport index page
    except:  
      all_product=Listing_data.objects.all() # all data face in database
      return render (request ,'index.html',{'all_product':all_product}) #  {} ->  data Deport index page


# ======================== Ragister fanction Email API ===================
def Register(request):
    
    # UkAJvmWX.NRrT13aTNQsG46oE0CYVsPSMm7vZB7uw
    if request.method == 'POST':         
        api_key = 'UkAJvmWX.NRrT13aTNQsG46oE0CYVsPSMm7vZB7uw' # Generated in your User Profile it shows at the top in a green bar once
        team_slug = "chiragkatrodiya1994" # when you sign up you have a team, its in the URL then use that
        email_address =request.POST['email'] #  user define email


        response = requests.post(
            "https://app.mailvalidation.io/a/" + team_slug + "/validate/api/validate/",
             json={'email': email_address},  
             headers={
                        'content-type': 'application/json',
                        'accept': 'application/json',
                        'Authorization': 'Api-Key ' + api_key,
                        },
            )

        valid = response.json()['is_valid'] 
        
        if valid:
            if request.POST['password'] == request.POST['Cpassword']: 
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
                return render (request,'otp.html',{'msg':'otp valid in 120 secound'})  
            else:
                return render (request,'Register.html',{'msg':'Password & Canfirm password do not match'})                
        else:
            return render (request,'Register.html',{"massage":'Invalid Email'})  
    else:
        return render (request,'Register.html')
     
# ======================== Search_for_products fanction ===================
           
def Search_for_products(request):
    user_data=Add_user.objects.get(email=request.session["email"])
    all_num=Cart.objects.filter(Q(Bayer_id=user_data.id) & Q(status=True))
    if request.method == 'POST':
        quary=request.POST['Search']
        all_product=Listing_data.objects.filter(Q(P_name__icontains=quary) | Q(P_Description__icontains=quary)) #  Q Use & oprater for maltipal condision 
        if all_product.count()==0:  # product count
            return render (request,"shop.html",{"msg":"sorry product not found.."})
        else:
            return render (request,"shop.html",{'all_product':all_product,'user_data':user_data})

# ======================== OTP fanction ===================

def otp(request):
    if request.method == "POST":
        if user_otp==int(request.POST["otp"]):
            end_time = datetime.now().time()   # current time
            time_diff = datetime.combine(datetime.today(),end_time) - datetime.combine(datetime.today(), start_time)   
            second_diff= time_diff.total_seconds() 
            if second_diff < 120:  #  otp time  
                Add_user.objects.create(         # data add to database
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
 
     
# ======================== Login fanction ===================

def Login(request):
    if request.method == 'POST': 
        try:   
            user_data=Add_user.objects.get(email=request.POST["email"]) # face singal data into database        
            if check_password(request.POST["password"],user_data.password)and(user_data.firstname==request.POST["firstname"]):
                request.session["email"] = request.POST["email"] # check current session & User email
                all_product=Listing_data.objects.all()
                return render(request,'shop.html',{'msg':user_data.firstname,'msg2':user_data.email,"all_product":all_product,"user_data":user_data})
            else:
                return render(request,'Login.html',{'msg':'sorry your Information  not match TRY AGEAN '})
        except:
            return render(request,'Login.html',{'msg':'User not exist plese registration'})
    else:
        return render(request,'Login.html')
 
            
 # ======================== Logout fanction ===================
                   
def Logout(request):
    del request.session["email"]   # delete session
    return render (request,'Login.html',{'msg':'User Logout successfully '})


 
# ======================== Profile fanction ===================
@login_required_custom    # use decoreter                  
def profile(request):
    user_data=Add_user.objects.get(email=request.session["email"])
    all_num=Cart.objects.filter(Q(Bayer_id=user_data.id) & Q(status=True))
    if request.method == 'POST': 
        profile_data=Add_user.objects.get(email=request.session['email'])
        try:
            profile_im=request.FILES["propic"]  # user image
        except:
            profile_im=profile_data.propic   # defult image
        if request.POST["new_password"]:
            if check_password(request.POST['Old_password'],profile_data.password):
                if request.POST['new_password'] == request.POST['Canform_new_Password']:
                    profile_data.password=make_password(request.POST['new_password']) # make password incript
                    profile_data.firstname=request.POST['firstname']
                    profile_data.propic=profile_im # update image
                    profile_data.save() # data save
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
        return render (request,'profile.html',{'profile_data':profile_data,"user_data":user_data,'all_num':all_num})
 
# ======================== shop fanction =================== 
@login_required_custom                        
def shop(request):
    user_data=Add_user.objects.get(email=request.session["email"])
    all_num=Cart.objects.filter(Q(Bayer_id=user_data.id) & Q(status=True)).count() 
    all_product=Listing_data.objects.all()
    return render (request,'shop.html',{"all_product":all_product ,'user_data': user_data,'all_num':all_num})



# ======================== Singal_product fanction ===================

def singal_product(request,ck):
    user_data=Add_user.objects.get(email=request.session["email"])
    all_num=Cart.objects.filter(Q(Bayer_id=user_data.id) & Q(status=True))
    one_product=Listing_data.objects.get(id=ck) # seller add product fech
    return render(request,'Shop_Detail.html',{"one_product":one_product,'all_num':all_num,'user_data':user_data,"sizes":one_product.P_size.split(","),"colors":one_product.P_Color.split(",")})
      #  listing "sizes":one_product.P_size.split(",") product Split


 # ======================== add to cart fanction ===================             
def Add_To_Cart(request,ck):
    Current_Login=Add_user.objects.get(email=request.session['email'])
    if request.method == 'POST':
        try:
            global all_num
            all_num=Cart.objects.all().count()
            Product=Listing_data.objects.get(id=ck)
            allredy_data=Cart.objects.get(Q(Product_id=ck) & Q(Bayer_id=Current_Login.id)) # check data allredy exit or not
            allredy_data.Quntity+=1  
            allredy_data.total=allredy_data.Quntity * allredy_data.Product_id.P_Price
            allredy_data.save()
            return Show_cart(request)  # return fanction 
        except:
            all_num=Cart.objects.all().count()
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
        

# ======================== Show cart fanction ===================

@login_required_custom   # use  Decorators
def Show_cart(request):
    user_data=Add_user.objects.get(email=request.session["email"])
    Current_Login=Add_user.objects.get(email=request.session["email"])
    all_num=Cart.objects.filter(Q(Bayer_id=Current_Login.id) & Q(status=True)).count()
    all_cart=Cart.objects.filter(Q(Bayer_id=Current_Login.id) & Q(status=True))
    total_amount=0
    Shipping_amount=0
    final_amount=0
    if all_cart.count()>0:
        for i in all_cart:
            total_amount+=i.total
            Shipping_amount=(total_amount*5)/100
            final_amount=total_amount+Shipping_amount   
    return render (request,'cart.html',{'all_cart':all_cart,'user_data': user_data,'total_amount':total_amount,"Shipping_amount":Shipping_amount,"final_amount":final_amount,'all_num':all_num})

  
# ======================== Remove_cart fanction ===================
def Remove_cart(request,ck):
    Cart_data=Cart.objects.get(id=ck)
    Cart_data.delete()
    return Show_cart(request)


# ======================== Update cart fanction ===================

def Update_cart(request):
    Current_Login=Add_user.objects.get(email=request.session["email"])
    if request.method == "POST":
        list_data=request.POST.getlist("UQuntity")   # getlist use in data to get in list forment
        all_cart=Cart.objects.filter(Q(Bayer_id=Current_Login.id) & Q(status=True)) 
        for i,j in zip(all_cart,list_data):
            i.Quntity=j
            i.total=int(j)*i.Product_id.P_Price
            i.save()
            print(all_cart)
            print(list_data)
        return Show_cart(request)
    else:
        return Show_cart(request)

# ======================== continue_shoping fanction ===================  
def continue_shoping(request):
    return shop(request)


# ======================== checkout fanction ===================
@login_required_custom                    
def checkout(request):
    # user_data=Add_user.objects.get(email=request.session["email"])
    # Current_Login=Add_user.objects.get(email=request.session["email"])
    # all_cart=Cart.objects.filter(Bayer_id=Current_Login.id)
    # total_amount=0
    # for i in all_cart:
    #     total_amount=total_amount+i.total
    #     Shipping_amount=(total_amount*5)/100 
    #     final_amount=total_amount+Shipping_amount   
    return render (request,'checkout.html')

 # ======================== checkoutdetail fanction ===================

def checkoutdetail(request):
    user_data=Add_user.objects.get(email=request.session["email"])
    all_num=Cart.objects.filter(Q(Bayer_id=user_data.id) & Q(status=True)).count()
    list1=['c','q','r','r','x','t' ,'_','5','6','9','9']
    a=random.choices(list1,k=10) 
    user_order="".join(a)   # create user id
    Current_Login=Add_user.objects.get(email=request.session["email"])
    if request.method == 'POST':
        
        try:
            one_data=checkout_detail.objects.get(bayer_detials=Current_Login)  #check data in save to database
        except:
            checkout_detail.objects.create(    # new data add in to database
                firstname=request.POST['fname'],
                lastname=request.POST['lname'],
                email=request.POST['email'],
                mobile_no=request.POST['mobile'],
                address1=request.POST['address1'],
                address2=request.POST['address2'],
                City=request.POST['city'],
                State=request.POST['State'],
                Country=request.POST['Country'],
                ZIPCode=request.POST['ZIPCode'],
                order_id=user_order,
                bayer_detials=user_data
        )
        
        one_data=checkout_detail.objects.get(bayer_detials=Current_Login)
        all_cart=Cart.objects.filter(Q(Bayer_id=Current_Login.id) & Q(status=True))
        for i in all_cart:
            i.Details_id=one_data
            i.save()
        return render(request,'order.html',{'one_data':one_data,"all_cart":all_cart,'all_num':all_num})
    else:
        return render (request,'checkout.html',{'msg':'open page','user_data':user_data,'all_num':all_num})
 
    
 # ======================== Payment fanction ===================
      
def payment(request):
    Current_Login=Add_user.objects.get(email=request.session["email"])
    all_cart=Cart.objects.filter(Bayer_id=Current_Login)
    total_amount=0
    final_amount=0
    Shipping_amount=0   
    for i in all_cart:
        total_amount=total_amount+i.total
        Shipping_amount=(total_amount*5)/100 
        final_amount=total_amount+Shipping_amount   
    return render (request,'payment.html',{'final_amount':final_amount,'all_cart':all_cart,'Shipping_amount':Shipping_amount,'total_amount':total_amount})


# ======================== all_delete fanction ===================
def all_delete(request):

    Current_Login=Add_user.objects.get(email=request.session["email"])
    all_cart=Cart.objects.filter(Q(Bayer_id=Current_Login.id) & Q(status=True))
    for i in all_cart:
        one_data=Listing_data.objects.get(id=i.Product_id.id)
        one_data.P_Quntity=int(one_data.P_Quntity)-i.Quntity
        i.status=False    # data cart in remove
        i.save()
        one_data.save()
    # all_cart.delete()
    # return render(request,"payment_success.html")
    return shop(request)
                   
# def order(request):
#     Current_Login=Add_user.objects.get(email=request.session["email"])
#     one_data=checkout_detail.objects.get(bayer_detials=Current_Login.id)
#     all_cart=Cart.objects.filter(Bayer_id=Current_Login.id)
#     return render(request,'seller_order.html',{'one_data':one_data,"all_cart":all_cart})


def API(request):
    url = "https://api.countrystatecity.in/v1/countries"
    headers = {
    "X-CSCAPI-KEY": "UXF2OHQ2WjBMT1Y5Q05MQzVhNE1sT3VJSk02Y3BaNzlRNHRVMHRjZA=="
    }
    mydata =  requests.request("GET", url, headers=headers)
    return render(request,'country.html',{"mydata":mydata.json()})
def single(request):
    url = "https://api.countrystatecity.in/v1/countries/BD"
    headers = {
    "X-CSCAPI-KEY": "UXF2OHQ2WjBMT1Y5Q05MQzVhNE1sT3VJSk02Y3BaNzlRNHRVMHRjZA=="
    }
    mydata = requests.request("GET", url, headers=headers)

# ======================== Categary fanction ===================

@login_required_custom
def Categary(request,ck):
    Current_Login=Add_user.objects.get(email=request.session["email"])
    # all_cart=Cart.objects.filter(Q(Bayer_id=Current_Login.id) & Q(status=False))
    all_product=Listing_data.objects.filter(P_Categary=ck)
    if all_product.count() == 0:
            return render (request,'shop.html',{'msg4':'Product Not Found'})

    return render (request,'shop.html',{'Current_Login':Current_Login,'all_product':all_product})


# ======================== contact fanction ===================

@login_required_custom
def contact(request):
    Current_Login=Add_user.objects.get(email=request.session["email"])
    return render (request,'contact.html',{'Current_Login':Current_Login})


# ======================== previous_order fanction ===================
@login_required_custom
def previous_order(request):
    Current_Login=Add_user.objects.get(email=request.session["email"])
    all_cart=Cart.objects.filter(Q(Bayer_id=Current_Login.id) & Q(status=False))
    return render (request,'previous_order.html',{'Current_Login':Current_Login,'all_cart':all_cart})
    
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
					return render(request, 'payment_success.html')
				except:

					# if there is an error while capturing payment.
					return render(request, 'paymentfail.html')
			else:

				# if signature verification fails.
				return render(request, 'paymentfail.html')
		except:

			# if we don't find the required parameters in POST data
			return all_delete(request)

	else:
	# if other than POST request is made.
		return render(request, 'paymentfail.html',{"msg":"ERROR2"})



















    
    