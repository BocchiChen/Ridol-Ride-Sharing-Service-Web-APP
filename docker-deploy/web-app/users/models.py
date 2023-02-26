from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
  user = models.OneToOneField(User, on_delete = models.CASCADE)
  gender = models.CharField(max_length = 11, default = '', blank=True)
  address = models.CharField(max_length = 100, default = '', blank=True)
  city = models.CharField(max_length = 100, default = '', blank=True)
  state = models.CharField(max_length = 100, default = '', blank=True)
  czip = models.CharField(max_length = 100, default = '', blank=True)
  
  class Meta:
    verbose_name = 'User Profile'
  
  def __str__(self):
    return "{}".format(self.user.__str__())
  
class DriverProfile(models.Model):
  driver = models.OneToOneField(User, on_delete = models.CASCADE)
  phone_num = models.CharField(max_length = 11, default = '', blank=True)
  car_type = models.CharField(max_length = 20, default = '', blank=True)
  license_number = models.CharField(max_length = 10, default = '', blank=True)
  max_capacity = models.PositiveIntegerField(default = 0)
  special_info = models.TextField(blank = True, default = '')
  
  class Meta:
    verbose_name = 'Driver Profile'
  
  def __str__(self):
    return "{}".format(self.driver.__str__())
    
@receiver(post_save, sender=User)
def create_user_info(sender, instance, created, **kwargs):
    if created:
        #UserProfile.objects.create(user=instance)
        DriverProfile.objects.create(driver=instance)

#@receiver(post_save, sender=User)
#def save_user_info(sender, instance, **kwargs):
    #instance.userprofile.save()
    #instance.driverprofile.save()


  
