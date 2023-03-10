from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserRegistrationForm, UserUpdateForm, UserUpdatePasswordForm, DriverRegistrationForm, DriverUpdateForm
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.contrib import messages
from .models import UserProfile, DriverProfile
from django.contrib.auth.models import User
from django.urls import reverse
from rides.models import RideOwner

def UserRegister(request):
  if request.method == 'GET':
    form = UserRegistrationForm()
    return render(request, 'users/regpage.html',{'form' : form})
  elif request.method == 'POST':
    form = UserRegistrationForm(request.POST)
    if form.is_valid():
      username = form.cleaned_data.get('username')
      email = form.cleaned_data.get('email')
      password = form.cleaned_data.get('password2')
      first_name = form.cleaned_data.get('first_name')
      last_name = form.cleaned_data.get('last_name')
      user = User.objects.create_user(username=username,email=email,password=password,first_name=first_name,last_name=last_name)
      gender = form.cleaned_data.get('gender')
      address = form.cleaned_data.get('address')
      city = form.cleaned_data.get('city')
      state = form.cleaned_data.get('state')
      czip = form.cleaned_data.get('czip')
      user_profile = UserProfile(user=user,gender=gender,address=address,city=city,state=state,czip=czip)
      user_profile.save()
      messages.success(request, f'Your account has been created. Please login now.')
      return redirect('UserLogin')
    else:
      print (form.errors)
      return render(request, 'users/regpage.html',{'form' : form})
      
def login(request):
  if request.method == 'POST':
    print(request.POST)
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = auth.authenticate(username = username, password = password)
    if user is not None and user.is_active:
      auth.login(request,user)
      mes = "Hello! "+user.last_name+" "+user.first_name+". How are doing today?"
      messages.success(request, mes)
      return redirect('Home')
    else:
      messages.warning(request, f'Username or password is not correct, please try again')
      return render(request,'users/loginpage.html')
  else:
     return render(request,'users/loginpage.html')

@login_required   
def logout(request):
  auth.logout(request)
  return render(request,'users/logoutpage.html')
      
@login_required
def DriverRegister(request):
  pk = request.user.id
  user = get_object_or_404(User,pk=pk)
  if request.method == 'GET':
    dp = get_object_or_404(DriverProfile,driver=user)
    form = DriverRegistrationForm(instance = dp)
    return render(request, 'users/dregpage.html',{'form' : form})
  elif request.method == 'POST':
    form = DriverRegistrationForm(instance = request.user.driverprofile, data = request.POST)
    if form.is_valid():
      #check valid
      dp = get_object_or_404(DriverProfile,driver=user)
      orders = RideOwner.objects.filter(driver_id = dp.id,status = 'confirmed')
      if orders.count() != 0 and (dp.phone_num != form.cleaned_data['phone_num'] or dp.car_type != form.cleaned_data['car_type'] or dp.license_number != form.cleaned_data['license_number'] or dp.max_capacity != form.cleaned_data['max_capacity'] or dp.special_info != form.cleaned_data['special_info']): 
        messages.warning(request, f'Your driver profile cannot be updated as you have confirmed orders. Please finish them first. ')
        return redirect('DriverComfirmed')
      #end check
      form.save()
      messages.success(request, f'Your driving account has been created. You can go and pick rides now.')
      return redirect('DriverHome')
    else:
      print (form.errors)
      return render(request, 'users/dregpage.html',{'form' : form})  

@login_required   
def UserChangePassword(request):
  pk = request.user.id
  user = get_object_or_404(User,pk=pk)
  if request.method == 'POST':
    form = UserUpdatePasswordForm(request.POST)
    if form.is_valid():
      if form.cleaned_data['password1'] == form.cleaned_data['password2']:
        new_password = form.cleaned_data['password2']
        user.set_password(new_password)
        user.save()
        messages.success(request, f'You have sucessfully changed your password.')
        return redirect('UserLogin')
      else:
        messages.warning(request, f"The two password fields didn't match! Please try again.")
        return render(request, 'users/passwordchange.html',{'form' : form})
    else:
      return render(request, 'users/passwordchange.html',{'form' : form})
  else:
    form = UserUpdatePasswordForm()
    return render(request, 'users/passwordchange.html',{'form' : form}) 

@login_required   
def UserEditInfo(request):
  pk = request.user.id
  user = get_object_or_404(User,pk=pk)
  user_profile = get_object_or_404(UserProfile,user=user)
  if request.method == 'POST':
    uf = UserUpdateForm(request.POST)
    df = DriverUpdateForm(instance = request.user.driverprofile, data = request.POST)
    if uf.is_valid() and df.is_valid():
      user.first_name = uf.cleaned_data['first_name']
      user.last_name = uf.cleaned_data['last_name']
      user.email = uf.cleaned_data['email']
      user.save()
      user_profile.gender = uf.cleaned_data['gender']
      user_profile.address = uf.cleaned_data['address']
      user_profile.city = uf.cleaned_data['city']
      user_profile.state = uf.cleaned_data['state']
      user_profile.czip = uf.cleaned_data['czip']
      user_profile.save()
      #check valid
      dp = get_object_or_404(DriverProfile,driver=user)
      orders = RideOwner.objects.filter(driver_id = dp.id,status = 'confirmed')
      if orders.count() != 0 and (dp.phone_num != df.cleaned_data['phone_num'] or dp.car_type != df.cleaned_data['car_type'] or dp.license_number != df.cleaned_data['license_number'] or dp.max_capacity != df.cleaned_data['max_capacity'] or dp.special_info != df.cleaned_data['special_info']): 
        messages.success(request, f'Your account information has been sucessfully updated. However, driver profile cannot be updated as you have confirmed orders. Please finish them first. ')
        return redirect('Home')
      #end check
      df.save()
      messages.success(request, f'Your account information has been sucessfully updated.')
      return redirect('Home')
    else:
      form = {'user_form' : uf, 'driver_form' : df}
      return render(request, 'users/profile.html', {'form' : form})
  else:
    default = {'email':user.email,'first_name':user.first_name,'last_name':user.last_name,'gender':user_profile.gender,'address':user_profile.address,
    'city':user_profile.city,'state':user_profile.state,'czip':user_profile.czip}
    uf = UserUpdateForm(default)
    df = DriverUpdateForm(instance=request.user.driverprofile)
    form = {'user_form' : uf, 'driver_form' : df}
    return render(request, 'users/profile.html', {'form' : form})
  
