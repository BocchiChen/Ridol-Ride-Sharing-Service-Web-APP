from django.contrib import admin
from .models import RideOwner, RideSharer

admin.site.register(RideOwner)
admin.site.register(RideSharer)
