from django.shortcuts import render, redirect, get_object_or_404
from .forms import RideOwnerForm, RideSharerForm
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.contrib import messages
from .models import RideOwner, RideSharer
from users.models import UserProfile, DriverProfile
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponseRedirect

def RenderHome(request):
  return render(request, 'rides/homepage.html')

@login_required
def RenderRideHome(request):
  if request.method == 'GET': 
    form1 = RideOwnerForm()
    form2 = RideSharerForm()
    return render(request, 'rides/ridehome.html',{'form1': form1, 'form2': form2, 'collapse1':'collapse show', 'collapse2':'collapse'})
  else: 
    pk = request.user.id
    user = get_object_or_404(User,pk=pk)
    #print(request.POST)
    if request.POST.get('searchsharebutton') is not None:
      print("ride sharer")
      form1 = RideOwnerForm()
      form2 = RideSharerForm(request.POST)
      if form2.is_valid():
        sha_destination = form2.cleaned_data['sha_destination']
        earliest_arrival_date = form2.cleaned_data['earliest_arrival_date']
        earliest_arrival_time = form2.cleaned_data['earliest_arrival_time']
        latest_arrival_date = form2.cleaned_data['latest_arrival_date']
        latest_arrival_time = form2.cleaned_data['latest_arrival_time']
        sha_tol_passengers = form2.cleaned_data['sha_tol_passengers']
        
        order_list = RideOwner.objects.filter(shared = True, status='open', 
        destination = sha_destination,
        arrival_date__gte=earliest_arrival_date,
        arrival_date__lte=latest_arrival_date
        ).exclude(rider=user).order_by('arrival_date')
        #print(order_list)
        order_list1 = order_list.filter().exclude(arrival_date=earliest_arrival_date,arrival_time__lte=earliest_arrival_time)
        order_list2 = order_list1.filter().exclude(arrival_date=latest_arrival_date,arrival_time__gte=latest_arrival_time)
        #exclude the order that user has already joined
        res = []
        for order in order_list2:
          share_order = RideSharer.objects.filter(sharer = user, order = order)
          if share_order.count() == 0:
            res.append(order)
          
        return render(request,'rides/orderforsharer.html',{'order_list':res,'a1':sha_destination,'a2':earliest_arrival_date,
        'a3':earliest_arrival_time,'a4':latest_arrival_date,'a5':latest_arrival_time,'a6':sha_tol_passengers})
      else:
        return render(request, 'rides/ridehome.html',{'form1': form1, 'form2': form2, 'collapse1':'collapse', 'collapse2':'collapse show'})
    else:
      print("ride owner")
      form1 = RideOwnerForm(request.POST)
      form2 = RideSharerForm()
      if form1.is_valid():
        ride_owner = RideOwner(
          destination = form1.cleaned_data['destination'],
          arrival_date = form1.cleaned_data['arrival_date'],
          arrival_time = form1.cleaned_data['arrival_time'],
          tol_passengers = form1.cleaned_data['tol_passengers'],
          tol_passenger_num = form1.cleaned_data['tol_passengers'],
          shared = form1.cleaned_data['shared'],
          vehicle_type = form1.cleaned_data['vehicle_type'],
          special_reqs = form1.cleaned_data['special_reqs']
        )
        ride_owner.rider = user
        ride_owner.save()
        messages.success(request, f'You have successfully made a Ridol Ride, please wait for a driver to pick your order.')
        return redirect('OrderInProcess') 
      else:
        return render(request, 'rides/ridehome.html',{'form1': form1, 'form2': form2, 'collapse1':'collapse show', 'collapse2':'collapse'})

#-------------------------------------------------------Ride Owner-----------------------------------------------------------------
@login_required
def RideOwnerNowList(request):
  pk = request.user.id
  user = get_object_or_404(User,pk=pk)
  confirmed_order = RideOwner.objects.filter(rider = user, status='confirmed').order_by('arrival_date')
  open_order = RideOwner.objects.filter(rider = user, status='open').order_by('arrival_date')
  return render(request, 'rides/orderinprocess.html', {'confirmed_order' : confirmed_order, 'open_order' : open_order})
    
@login_required
def RideOwnerEditOrder(request, oid):
  order = RideOwner.objects.filter(pk = oid).first()
  if request.method == 'POST':
    if request.POST.get('tol_passengers2') is not None:
      if int(request.POST.get('tol_passengers2')) <= 0:
        messages.warning(request, f'You cannot import a non-positive passenger number!')
        return redirect('OrderInProcess')
      order.tol_passenger_num -= order.tol_passengers
      order.tol_passengers = int(request.POST.get('tol_passengers2'))
      order.tol_passenger_num += int(request.POST.get('tol_passengers2'))
      order.save()
      messages.success(request, f'You have successfully modified the order.')
      return redirect('OrderInProcess')
    form = RideOwnerForm(request.POST)
    if form.is_valid():
      order.destination = form.cleaned_data['destination']
      order.arrival_date = form.cleaned_data['arrival_date']
      order.arrival_time = form.cleaned_data['arrival_time']
      order.tol_passenger_num -= order.tol_passengers
      order.tol_passengers = form.cleaned_data['tol_passengers']
      order.tol_passenger_num += form.cleaned_data['tol_passengers']
      order.shared = form.cleaned_data['shared']
      order.vehicle_type = form.cleaned_data['vehicle_type']
      order.special_reqs = form.cleaned_data['special_reqs']
      order.save()
      messages.success(request, f'You have successfully modified the order.')
      return redirect('OrderInProcess')
    else:
      return render(request, 'rides/orderinfo.html', {'form' : form})
  else:
    default = {'destination':order.destination,'arrival_date':order.arrival_date,'arrival_time':order.arrival_time,'tol_passengers':order.tol_passengers,'shared':order.shared,
    'vehicle_type':order.vehicle_type,'special_reqs':order.special_reqs}
    form = RideOwnerForm(default)
    sharer = RideSharer.objects.filter(order_id = oid)
    if sharer.count() == 0:
      return render(request, 'rides/orderinfo.html', {'form' : form})
    else:
      messages.warning(request, f'Oops! Seems like some sharers have already joined your ride, you can only change the passenger number or cancel the ride if you want.')
      return render(request, 'rides/orderinfo2.html', {'form' : default})

@login_required
def RideOwnerDeleteOrder(request, oid):
  order = RideOwner.objects.filter(pk = oid).first()
  order.delete()
  messages.success(request, f'You have successfully cancelled the order. All the related sharers quit.')
  return redirect('OrderInProcess')
    
@login_required
def RideOwnerHistoryList(request):
  pk = request.user.id
  user = get_object_or_404(User,pk=pk)
  order_list = RideOwner.objects.filter(rider = user, status='complete').order_by('-arrival_date')
  share_orders = RideSharer.objects.filter(sharer = user)
  share_rideowner_order = []
  for obj in share_orders:
    if obj.order.status == 'complete':
      share_rideowner_order.append(RideOwner.objects.filter(id = obj.order_id,status = 'complete')[0])
  share_rideowner_order.sort(key = lambda x : x.arrival_date,reverse = True)
  return render(request,'rides/orderhistory.html',{'user':user,'order_list':order_list,'share_rideowner_order':share_rideowner_order})
    
#--------------------------------------------------------Driver-------------------------------------------------------------------- 
@login_required
def DriverViewOpenList(request):
  pk = request.user.id
  user = get_object_or_404(User,pk=pk)
  dp = get_object_or_404(DriverProfile,driver=user)
  if dp.phone_num == '' or dp.car_type == '' or dp.license_number == '' or dp.max_capacity == '':
    messages.warning(request, f"Seems like you don't finish or make your driver profile :<, please take some minutes to fill in the following form.")
    return redirect('DriverRegister')
  open_order = RideOwner.objects.filter(status='open',tol_passenger_num__lte = dp.max_capacity,special_reqs=dp.special_info,
  vehicle_type__in = ['',dp.car_type]).exclude(rider=user).order_by('arrival_date')
  #driver cannot pick the shared orders joined by him
  res = []
  for order in open_order:
    share_order = RideSharer.objects.filter(sharer = user, order = order)
    if share_order.count() == 0:
      res.append(order)
  return render(request,'rides/driverhome.html',{'user':user,'open_order':res})

@login_required
def DriverWorkingList(request):
  pk = request.user.id
  user = get_object_or_404(User,pk=pk)
  dp = get_object_or_404(DriverProfile,driver=user)
  if dp.phone_num == '' or dp.car_type == '' or dp.license_number == '' or dp.max_capacity == '':
    messages.warning(request, f"Seems like you don't finish or make your driver profile :<, please take some minutes to fill in the following form.")
    return redirect('DriverRegister')
  comfirmed_order = RideOwner.objects.filter(driver = user.driverprofile, status='confirmed').order_by('arrival_date')
  return render(request,'rides/drivercomfirmed.html',{'user':user,'comfirmed_order':comfirmed_order})
    
@login_required
def DriverConfirmOrder(request, oid):
  pk = request.user.id
  user = get_object_or_404(User,pk=pk)
  dp = get_object_or_404(DriverProfile,driver=user)
  if dp.phone_num == '' or dp.car_type == '' or dp.license_number == '' or dp.max_capacity == '':
    messages.warning(request, f"Seems like you don't finish or make your driver profile :<, please take some minutes to fill in the following form.")
    return redirect('DriverRegister')
  driver_profile = get_object_or_404(DriverProfile,driver=user)
  order = RideOwner.objects.filter(pk = oid).first()
  conditions = True
  if order.tol_passenger_num > driver_profile.max_capacity:
    conditions = False
    messages.warning(request, f"You can't pick this order. Maximum capacity of your car is not enough!")
  if order.vehicle_type != '' and order.vehicle_type != driver_profile.car_type:
    conditions = False
    messages.warning(request, f"You can't pick this order. Your vehicle type doesn't fit owner's requirement!")
  if order.special_reqs != driver_profile.special_info:
    conditions = False
    messages.warning(request, f"You can't pick this order. The special requirements of you or the ride owner don't match!")
  if conditions:
    order.status = 'confirmed'
    order.driver = user.driverprofile
    order.vehicle_type = dp.car_type
    order.save()
    mes = "You have sucessfully pick the order of " + order.rider.username + "!"
    messages.success(request, mes)
    #-------------send email added--------------------
    rider = get_object_or_404(User,pk=order.rider.id)
    print(rider.email)
    subject = 'Message from Ridol~: Your order has been confirmed.'
    message = f'Hi {rider}, thank you for choosing Ridol~. {user} have confirmed your Ridol Ride! Respond to give us your feedback.'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [rider.email, ]
    send_mail( subject, message, email_from, recipient_list )
    subject = 'Message from Ridol~: Your order has been confirmed.'
    message = f'Hi {user}, You have confirmed the Ridol Ride owned by {rider}! Respond to give us your feedback.'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [user.email, ]
    send_mail( subject, message, email_from, recipient_list )


    sharerorder=RideSharer.objects.filter(order_id = order.id)
    for sharerorderobj in sharerorder:
      sharer = get_object_or_404(User,pk=sharerorderobj.sharer_id)
      subject = 'Message from Ridol~: Your sharer order has been confirmed.'
      message = f'Hi {sharer}, Your sharer order have been confirmed by {user}! Respond to give us your feedback.'
      email_from = settings.EMAIL_HOST_USER
      recipient_list = [sharer.email]
      send_mail( subject, message, email_from, recipient_list )
    
    return redirect('DriverComfirmed')
  return redirect('DriverHome')

@login_required
def DriverCompleteOrder(request, oid):
  pk = request.user.id
  user = get_object_or_404(User,pk=pk)
  dp = get_object_or_404(DriverProfile,driver=user)
  if dp.phone_num == '' or dp.car_type == '' or dp.license_number == '' or dp.max_capacity == '':
    messages.warning(request, f"Seems like you don't finish or make your driver profile :<, please take some minutes to fill in the following form.")
    return redirect('DriverRegister')
  order = RideOwner.objects.filter(pk = oid).first()
  order.status = 'complete'
  order.save()
  mes = "Congratulations! You have completed the Ridol Ride of " + order.rider.username + " :)"
  messages.success(request, mes)
  return redirect('CompleteOrder')

@login_required
def DriverHistoryList(request):
  pk = request.user.id
  user = get_object_or_404(User,pk=pk) 
  dp = get_object_or_404(DriverProfile,driver=user)
  if dp.phone_num == '' or dp.car_type == '' or dp.license_number == '' or dp.max_capacity == '':
    messages.warning(request, f"Seems like you don't finish or make your driver profile :<, please take some minutes to fill in the following form.")
    return redirect('DriverRegister')
  complete_order = RideOwner.objects.filter(driver = user.driverprofile, status='complete').order_by('arrival_date')
  return render(request,'rides/drivercompleteorder.html',{'user':user,'complete_order':complete_order})
    
#------------------------------------------------------Ride Sharer-----------------------------------------------------------------

@login_required
def SharerJoinOrder(request, oid, a1, a2, a3, a4, a5, a6):
  pk = request.user.id
  user = get_object_or_404(User,pk=pk)
  ride_sharer = RideSharer(
    sha_destination = a1,
    earliest_arrival_date = a2,
    earliest_arrival_time = a3,
    latest_arrival_date = a4,
    latest_arrival_time = a5,
    sha_tol_passengers = a6
  )
  ride_sharer.sharer = user
  ride_sharer.save()
  order = RideOwner.objects.filter(pk = oid).first()
  order.tol_passenger_num += ride_sharer.sha_tol_passengers
  order.save()
  ride_sharer.order = order
  ride_sharer.save()
  mes = "You have joined the Ridol Ride hosted by " + order.rider.username + " :)"
  messages.success(request, mes)
  return redirect('SharerNowList')

@login_required
def SharerCancelOrder(request, oid):
  pk = request.user.id
  user = get_object_or_404(User,pk=pk)
  order = RideSharer.objects.filter(sharer = user, order_id = oid).first()
  owner = order.order
  owner.tol_passenger_num -= order.sha_tol_passengers
  owner.save()
  order.delete()
  mes = "You have successfully quit the Ridol ride of "+order.order.rider.username+" :)"
  messages.success(request, mes)
  return redirect('SharerNowList')
  
@login_required
def SharerEditOrder(request, oid):
  pk = request.user.id
  user = get_object_or_404(User,pk=pk)
  shareorder = RideSharer.objects.filter(sharer = user,order_id = oid).first()
  ownerorder = shareorder.order
  if request.method == 'POST':
    if int(request.POST.get('sha_tol_passengers')) <= 0:
      messages.warning(request, f'You cannot import a non-positive passenger number!')
      return redirect('SharerNowList')
    passengersnum = request.POST.get('sha_tol_passengers')
    ownerorder.tol_passenger_num = ownerorder.tol_passenger_num - shareorder.sha_tol_passengers + int(passengersnum)
    ownerorder.save()
    shareorder.sha_tol_passengers = int(passengersnum)
    shareorder.save()
    messages.success(request, f'You have successfully modified the order.')
    return redirect('SharerNowList')
  else:
    form = {'sha_destination':shareorder.sha_destination,'earliest_arrival_date':shareorder.earliest_arrival_date,'latest_arrival_date':shareorder.latest_arrival_date,'earliest_arrival_time':shareorder.earliest_arrival_time,'latest_arrival_time':shareorder.latest_arrival_time,
    'sha_tol_passengers':shareorder.sha_tol_passengers}
    #form1 = RideSharerForm(form)
    return render(request, 'rides/sharerorderinfo.html', {'form' : form})

@login_required
def SharerNowList(request): 
  pk = request.user.id
  user = get_object_or_404(User,pk=pk)
  shared_order = RideSharer.objects.filter(sharer = user)
  share_open_order =[]
  share_comfirmed_order =[]
  for obj in shared_order:
    if obj.order is not None:
      if obj.order.status == 'open':    
        share_open_order.append(RideOwner.objects.filter(id = obj.order_id,status = 'open')[0])
      elif obj.order.status == 'confirmed':
        share_comfirmed_order.append(RideOwner.objects.filter(id = obj.order_id,status = 'confirmed')[0])     
      #share_comfirmed_order.append(obj)
  share_open_order.sort(key = lambda x : x.arrival_date)
  share_comfirmed_order.sort(key = lambda x : x.arrival_date)
  return render(request, 'rides/shareoderinprocess.html', {'share_open_order':share_open_order,'share_comfirmed_order':share_comfirmed_order})

@login_required
def OrderDetail(request,oid):
  if request.method=='GET':
    pk = request.user.id
    user = get_object_or_404(User,pk=pk)
    owner_order = RideOwner.objects.filter(pk = oid).first() 
    shared_order = RideSharer.objects.filter(order_id = oid)
    return render(request,'rides/orderdetail.html',{'owner_order':owner_order,'shared_order':shared_order})
  else:
    next = request.POST.get('next', '/')
    return redirect(next)
 
@login_required
def RenderPassengerInfo(request, oid):
  if request.method =='GET':
    pk = request.user.id
    user = get_object_or_404(User,pk=pk)
    owner_order = RideOwner.objects.filter(pk = oid).first()
    sharers = RideSharer.objects.filter(order = owner_order)
    return render(request,'rides/ridepassengernumber.html',{'owner_order':owner_order,'sharers':sharers})
  else:
    next = request.POST.get('next', '/')
    return redirect(next)
@login_required
def RenderDriverPassengersInfo(request, oid):
  if request.method =='GET':
    pk = request.user.id
    user = get_object_or_404(User,pk=pk)
    owner_order = RideOwner.objects.filter(pk = oid).first()
    sharers = RideSharer.objects.filter(order = owner_order)
    return render(request,'rides/driverpassengernumber.html',{'owner_order':owner_order,'sharers':sharers})
  else:
      next = request.POST.get('next', '/')
      return redirect(next)

