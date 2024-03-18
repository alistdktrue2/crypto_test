from django.contrib import admin
from .models import Comerciante,Subscription,Bancos
# Register your models here.


admin.site.register(Comerciante)
admin.site.register(Bancos)
#admin.site.register(Subscription)