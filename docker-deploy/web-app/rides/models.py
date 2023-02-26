from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from users.models import DriverProfile

class RideOwner(models.Model):
  rider = models.ForeignKey(User, on_delete=models.CASCADE)
  destination = models.CharField(max_length = 100,default = '')
  arrival_date = models.DateField(null = True, blank = True)
  arrival_time = models.TimeField(null = True, blank = True)
  tol_passengers = models.PositiveIntegerField(default = 1)
  tol_passenger_num = models.PositiveIntegerField(default = 0)
  status = models.CharField(default='open', max_length=20)
  shared = models.BooleanField(default = False)
  vehicle_type = models.CharField(max_length = 20, default = '',blank=True)
  special_reqs = models.TextField(blank = True, default = '')
  driver = models.ForeignKey(DriverProfile,on_delete=models.CASCADE,null=True,blank=True)
  
  class Meta:
    verbose_name = 'Ride Detail'
  
  def __str__(self):
    return "{}".format(self.rider.__str__())
    
class RideSharer(models.Model):
  sharer = models.ForeignKey(User, on_delete=models.CASCADE)
  sha_destination = models.CharField(max_length = 100,default = '')
  earliest_arrival_date = models.DateField(null = True, blank = True)
  earliest_arrival_time = models.TimeField(null = True, blank = True)
  latest_arrival_date = models.DateField(null = True, blank = True)
  latest_arrival_time = models.TimeField(null = True, blank = True)
  sha_tol_passengers = models.PositiveIntegerField(default = 1)
  order = models.ForeignKey(RideOwner,on_delete=models.CASCADE,null=True,blank=True)

  class Meta:
    verbose_name = 'Share Detail'
  
  def __str__(self):
    return "{}".format(self.sharer.__str__())
    
