from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import AbstractUser, User
from django.conf import settings
from django.contrib.auth import get_user_model

def get_default_user():
    default_user = get_user_model().objects.first()
    return default_user.id if default_user else None

class CustomUser(AbstractUser):
    """
    Rozšířený uživatelský model s preferencemi pro měsíční reporty.
    """
    receive_monthly_reports = models.BooleanField(default=False)
    email_for_reports = models.EmailField(null=True, blank=True)

    class Meta:
        swappable = 'AUTH_USER_MODEL'

class Akcie(models.Model):
    """
    Model reprezentující akcie s detaily o počtu, ceně a zisku/ztrátě.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='akcie', default=get_default_user)
    nazev = models.CharField(max_length=100)
    datum = models.DateField(default=now)
    cas = models.TimeField(default=now)
    pocet_ks = models.IntegerField()
    cena_za_kus = models.DecimalField(max_digits=10, decimal_places=2)
    hodnota = models.DecimalField(max_digits=15, decimal_places=2)
    nakup = models.DecimalField(max_digits=15, decimal_places=2)
    zisk_ztrata = models.DecimalField(max_digits=15, decimal_places=2)
    dividenda = models.DecimalField(max_digits=15, decimal_places=2)

    def __str__(self):
        return self.nazev

class Transakce(models.Model):
    akcie = models.ForeignKey(Akcie, on_delete=models.CASCADE)
    datum = models.DateField()
    typ = models.CharField(max_length=50, choices=[('nákup', 'Nákup'), ('prodej', 'Prodej')])
    mnozstvi = models.IntegerField()
    cena = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.typ} - {self.akcie.nazev}"

class Dividenda(models.Model):
    akcie = models.ForeignKey(Akcie, on_delete=models.CASCADE, related_name='dividendy')
    datum = models.DateField()
    castka = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Dividenda - {self.akcie.nazev}"

class Aktivita(models.Model):
    akce = models.CharField(max_length=255)
    uzivatel = models.CharField(max_length=255, null=True, blank=True)
    datum_cas = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.akce} ({self.datum_cas})"
