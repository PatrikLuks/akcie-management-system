from django.contrib import admin
from .models import Akcie, Transakce, Dividenda, AuditLog

# Register your models here.
admin.site.register(Akcie)
admin.site.register(Transakce)
admin.site.register(Dividenda)
admin.site.register(AuditLog)
