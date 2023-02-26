from django.urls import path
from django.shortcuts import render
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.RenderHome, name = 'GoHome'),
    path('home/', views.RenderHome, name = 'Home'),
    path('users/ridehome/', views.RenderRideHome, name='RideHome'),
    path('users/ride-owner/order-info/<int:oid>', views.RideOwnerEditOrder, name='OwnerEditOrder'),
    path('users/ride-owner/delete-order/<int:oid>', views.RideOwnerDeleteOrder, name='OwnerDeleteOrder'),
    path('users/ride-owner/orderhistory/', views.RideOwnerHistoryList, name='OrderHistory'),  
    path('users/ride-owner/orderinprocess/', views.RideOwnerNowList, name='OrderInProcess'), 
    path('users/driver/driverhome/', views.DriverViewOpenList, name='DriverHome'), 
    path('users/driver/drivercomfirmed/', views.DriverWorkingList, name='DriverComfirmed'),
    path('users/driver/order-comfirm/<int:oid>', views.DriverConfirmOrder, name='DriverConfirmProcess'), 
    path('users/driver/order-complete/<int:oid>', views.DriverCompleteOrder, name='DriverCompleteProcess'),   
    path('users/driver/complete-order/', views.DriverHistoryList, name='CompleteOrder'),  
    path('users/ride-sharer/join-order/<int:oid>/<str:a1>/<str:a2>/<str:a3>/<str:a4>/<str:a5>/<int:a6>', views.SharerJoinOrder, name='SharerJoinAOrder'), 
    path('users/ride-sharer/quit-order/<int:oid>', views.SharerCancelOrder, name='SharerCancelAOrder'),
    path('users/ride-owner/order-passenger-info/<int:oid>', views.RenderPassengerInfo, name='RenderPassengersInfo'),
    path('users/driver/order-driverpassenger-info/<int:oid>', views.RenderDriverPassengersInfo, name='RenderDriverPassengersInfo'),
    path('users/ride-sharer/sharerorderinprocess', views.SharerNowList, name='SharerNowList'),
    path('users/ride-sharer/sharerorder-info/<int:oid>', views.SharerEditOrder, name='SharerEditOrder'),
    path('users/orderdetail/<int:oid>',views.OrderDetail,name = 'OrderDetail'),
]
