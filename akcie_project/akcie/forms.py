from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.utils.timezone import now
from pytz import timezone
from .models import Akcie, Transakce, Dividenda, CustomUser

class AkcieForm(forms.ModelForm):
    prague_tz = timezone('Europe/Prague')
    datum = forms.DateField(label='Datum', widget=forms.DateInput(attrs={'type': 'date'}), initial=now().astimezone(prague_tz).date)
    cas = forms.TimeField(label='Čas', widget=forms.TimeInput(attrs={'type': 'time'}), initial=now().astimezone(prague_tz).time)
    pocet_ks = forms.IntegerField(label='Počet kusů')

    class Meta:
        model = Akcie
        fields = ['nazev', 'datum', 'cas', 'pocet_ks']

class TransakceForm(forms.ModelForm):
    akcie = forms.ChoiceField(choices=[], label='Akcie')

    class Meta:
        model = Transakce
        fields = ['akcie', 'datum', 'mnozstvi']

    def __init__(self, *args, **kwargs):
        akcie_choices = kwargs.pop('akcie_choices', [])
        super().__init__(*args, **kwargs)
        self.fields['akcie'].choices = akcie_choices

class DividendaForm(forms.ModelForm):
    class Meta:
        model = Dividenda
        fields = ['akcie', 'datum', 'castka']

class CustomUserForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'receive_monthly_reports', 'email_for_reports')