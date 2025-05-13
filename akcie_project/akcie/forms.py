from django import forms
from .models import Akcie, Transakce, Dividenda

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