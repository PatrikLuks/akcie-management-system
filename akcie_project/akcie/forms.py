from django import forms
from django.contrib.auth.forms import UserChangeForm
from .models import Akcie, Transakce, Dividenda, CustomUser

class AkcieForm(forms.ModelForm):
    class Meta:
        model = Akcie
        fields = ['nazev', 'pocet_ks', 'cena_za_kus', 'hodnota', 'nakup', 'zisk_ztrata', 'dividenda']

class TransakceForm(forms.ModelForm):
    class Meta:
        model = Transakce
        fields = ['akcie', 'datum', 'typ', 'mnozstvi', 'cena']

class DividendaForm(forms.ModelForm):
    class Meta:
        model = Dividenda
        fields = ['akcie', 'datum', 'castka']

class CustomUserForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'receive_monthly_reports', 'email_for_reports')