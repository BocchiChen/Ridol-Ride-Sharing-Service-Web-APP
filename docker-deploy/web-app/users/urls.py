from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('register/', views.UserRegister, name='UserRegister'),
    path('login/', views.login, name='UserLogin'),
    path('logout/', views.logout, name='UserLogout'),
    path('users/driver-register/', views.DriverRegister, name='DriverRegister'),
    path('users/info/', views.UserEditInfo, name='UserInfo'),
    path('users/change-password/', views.UserChangePassword, name='PassInfo'),
]
  
