from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import RideOwner, RideSharer
  
class RideOwnerForm(forms.ModelForm):
  
  destination = forms.CharField(max_length=100, required=True, error_messages={'max_length':'Maximum length of destination address cannot be greater than 100!', 'required':'Destination address is required!'}, widget=forms.TextInput(attrs={'placeholder':'Please enter your destination address','class':'form-control'}), label = 'Destination Address:')
  
  arrival_date = forms.DateField(required=True, input_formats = ['%Y-%m-%d'], error_messages={'required':'Arrival date is required!'}, widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}), label = 'Arrival Date:')
  
  arrival_time = forms.TimeField(required=True, input_formats = ['%H:%M'], error_messages={'required':'Arrival time is required!'}, widget=forms.TimeInput(format='%H:%M', attrs={'type': 'time'}), label = 'Arrival Time:')
  
  vehicle_type = forms.CharField(max_length=20, required=False, error_messages={'max_length':'Maximum length of vehicle type cannot be greater than 20!'}, widget=forms.TextInput(attrs={'placeholder':'(Optional)','class':'form-control'}), label = 'Vehicle Type:')
  
  tol_passengers = forms.IntegerField(min_value=1, required=True, error_messages={'min_value':'Total number of passengers should at least be one!', 'required':'Total number of passengers is required!'}, widget=forms.NumberInput(attrs={'placeholder':'1','class':'form-control'}), label = 'Total Number Of Passengers:')
    
  shared = forms.BooleanField(required = False, label = 'Share Or Not:')
  
  special_reqs = forms.CharField(max_length=200, required=False, error_messages={'max_length':'Maximum length of special requests cannot be greater than 200!'}, widget=forms.Textarea(attrs={'placeholder':'Leave a request here','class':'form-control'}), label = 'Special Request:')
  
  class Meta:
    model = RideOwner
    fields = ['destination', 'arrival_date', 'arrival_time', 'vehicle_type', 'tol_passengers', 'shared', 'special_reqs']
    
class RideSharerForm(forms.ModelForm):
  
  sha_destination = forms.CharField(max_length=100, required=True, error_messages={'max_length':'Maximum length of destination address cannot be greater than 100!', 'required':'Destination address is required!'}, widget=forms.TextInput(attrs={'placeholder':'Please enter your destination address','class':'form-control'}), label = 'Destination Address:')
  
  earliest_arrival_date = forms.DateField(required=True, input_formats = ['%Y-%m-%d'], error_messages={'required':'Earliest arrival date is required!'}, widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}), label = 'Earliest Arrival Date:')
  
  latest_arrival_date = forms.DateField(required=True, input_formats = ['%Y-%m-%d'], error_messages={'required':'Latest arrival date is required!'}, widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}), label = 'Latest Arrival Date:')
  
  earliest_arrival_time = forms.TimeField(required=True, input_formats = ['%H:%M'], error_messages={'required':'Earliest arrival time is required!'}, widget=forms.TimeInput(format='%H:%M', attrs={'type': 'time'}), label = 'Earliest Arrival Time:')
  
  latest_arrival_time = forms.TimeField(required=True, input_formats = ['%H:%M'], error_messages={'required':'Latest arrival time is required!'}, widget=forms.TimeInput(format='%H:%M', attrs={'type': 'time'}), label = 'Latest Arrival Time:')
  
  sha_tol_passengers = forms.IntegerField(min_value=1, required=True, error_messages={'min_value':'Total number of passengers should at least be one!', 'required':'Total number of passengers is required!'}, widget=forms.NumberInput(attrs={'placeholder':'Please enter the total number of passengers','class':'form-control'}), label = 'Total Number Of Passengers:')
    
  class Meta:
    model = RideSharer
    fields = ['sha_destination', 'earliest_arrival_date', 'earliest_arrival_time', 'latest_arrival_date', 'latest_arrival_time', 'sha_tol_passengers']
  
