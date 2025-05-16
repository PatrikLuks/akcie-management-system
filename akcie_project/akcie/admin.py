from django.contrib import admin
from .models import Akcie, Transakce, Dividenda, AuditLog, Klient, Portfolio

class KlientAdmin(admin.ModelAdmin):
    list_display = ('jmeno', 'prijmeni', 'email', 'poradce')
    search_fields = ('jmeno', 'prijmeni', 'email')
    list_filter = ('poradce',)

class PortfolioAdmin(admin.ModelAdmin):
    list_display = ('nazev', 'klient', 'datum_vytvoreni')
    search_fields = ('nazev', 'klient__jmeno', 'klient__prijmeni')
    list_filter = ('klient',)

admin.site.register(Akcie)
admin.site.register(Transakce)
admin.site.register(Dividenda)
admin.site.register(AuditLog)
admin.site.register(Klient, KlientAdmin)
admin.site.register(Portfolio, PortfolioAdmin)
