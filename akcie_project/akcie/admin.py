from django.contrib import admin
from .models import Akcie, Transakce, Dividenda

# Register your models here.
admin.site.register(Akcie)
admin.site.register(Transakce)
admin.site.register(Dividenda)
