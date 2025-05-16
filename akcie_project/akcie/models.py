from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import AbstractUser, User
from django.conf import settings
from django.contrib.auth import get_user_model
import json

def get_default_user():
    default_user = get_user_model().objects.first()
    return default_user.id if default_user else None

class CustomUser(AbstractUser):
    """
    Rozšířený uživatelský model s preferencemi pro měsíční reporty.
    """
    receive_monthly_reports = models.BooleanField(default=True, verbose_name="Zasílat měsíční PDF report e-mailem")
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
    ticker = models.CharField(max_length=20, null=True, blank=True, help_text="Oficiální ticker akcie dle burzy (např. AAPL pro Apple Inc.)")
    mena = models.CharField(max_length=8, null=True, blank=True, default='CZK', help_text="Měna, ve které je akcie obchodována (např. USD, EUR, CZK)")

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

class AuditLog(models.Model):
    model_name = models.CharField(max_length=64)
    object_id = models.PositiveIntegerField()
    action = models.CharField(max_length=16)  # create, update, delete
    changes = models.TextField(blank=True)  # JSON diff
    user = models.ForeignKey(get_user_model(), null=True, blank=True, on_delete=models.SET_NULL)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.model_name} {self.object_id} {self.action} {self.timestamp}"

class Klient(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name='klient_profile')
    jmeno = models.CharField(max_length=100)
    prijmeni = models.CharField(max_length=100)
    email = models.EmailField()
    telefon = models.CharField(max_length=30, blank=True)
    adresa = models.CharField(max_length=255, blank=True)
    datum_vytvoreni = models.DateTimeField(auto_now_add=True)
    poznamka = models.TextField(blank=True)
    poradce = models.ForeignKey(get_user_model(), null=True, blank=True, on_delete=models.SET_NULL, related_name='klienti', help_text='Poradce, který spravuje tohoto klienta')

    def __str__(self):
        return f"{self.jmeno} {self.prijmeni} ({self.email})"

class Portfolio(models.Model):
    klient = models.ForeignKey(Klient, on_delete=models.CASCADE, related_name='portfolia')
    nazev = models.CharField(max_length=100)
    popis = models.TextField(blank=True)
    datum_vytvoreni = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nazev} - {self.klient}"

# --- Audit logika pro Akcie, Transakce, Dividenda ---
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

def get_changes(instance, created):
    data = {}
    for field in instance._meta.fields:
        data[field.name] = str(getattr(instance, field.name))
    return json.dumps(data, ensure_ascii=False)

@receiver(post_save, sender=Akcie)
def audit_akcie_save(sender, instance, created, **kwargs):
    AuditLog.objects.create(
        model_name='Akcie',
        object_id=instance.pk,
        action='create' if created else 'update',
        changes=get_changes(instance, created),
        user=getattr(instance, 'user', None)
    )

@receiver(post_delete, sender=Akcie)
def audit_akcie_delete(sender, instance, **kwargs):
    AuditLog.objects.create(
        model_name='Akcie',
        object_id=instance.pk,
        action='delete',
        changes=get_changes(instance, False),
        user=getattr(instance, 'user', None)
    )

@receiver(post_save, sender=Transakce)
def audit_transakce_save(sender, instance, created, **kwargs):
    AuditLog.objects.create(
        model_name='Transakce',
        object_id=instance.pk,
        action='create' if created else 'update',
        changes=get_changes(instance, created),
        user=None
    )

@receiver(post_delete, sender=Transakce)
def audit_transakce_delete(sender, instance, **kwargs):
    AuditLog.objects.create(
        model_name='Transakce',
        object_id=instance.pk,
        action='delete',
        changes=get_changes(instance, False),
        user=None
    )

@receiver(post_save, sender=Dividenda)
def audit_dividenda_save(sender, instance, created, **kwargs):
    AuditLog.objects.create(
        model_name='Dividenda',
        object_id=instance.pk,
        action='create' if created else 'update',
        changes=get_changes(instance, created),
        user=None
    )

@receiver(post_delete, sender=Dividenda)
def audit_dividenda_delete(sender, instance, **kwargs):
    AuditLog.objects.create(
        model_name='Dividenda',
        object_id=instance.pk,
        action='delete',
        changes=get_changes(instance, False),
        user=None
    )
