from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.utils.timezone import now
from pytz import timezone
from .models import Akcie, Transakce, Dividenda, CustomUser, Klient, Portfolio

class AkcieForm(forms.ModelForm):
    prague_tz = timezone('Europe/Prague')
    datum = forms.DateField(label='Datum', widget=forms.DateInput(attrs={'type': 'date'}), initial=now().astimezone(prague_tz).date)
    cas = forms.TimeField(label='Čas', widget=forms.TimeInput(attrs={'type': 'time'}), initial=now().astimezone(prague_tz).time)
    pocet_ks = forms.IntegerField(label='Počet kusů', min_value=1, error_messages={'min_value': 'Počet kusů musí být větší než 0.'})
    cena_za_kus = forms.DecimalField(label='Cena za kus', max_digits=10, decimal_places=2, min_value=0, error_messages={'min_value': 'Cena musí být nezáporná.'})
    hodnota = forms.DecimalField(label='Hodnota', max_digits=15, decimal_places=2, required=False, min_value=0)
    nakup = forms.DecimalField(label='Nákup', max_digits=15, decimal_places=2, required=False, min_value=0)
    zisk_ztrata = forms.DecimalField(label='Zisk/Ztráta', max_digits=15, decimal_places=2, required=False)

    class Meta:
        model = Akcie
        fields = ['nazev', 'datum', 'cas', 'pocet_ks', 'cena_za_kus', 'hodnota', 'nakup', 'zisk_ztrata']

    def clean_nazev(self):
        nazev = self.cleaned_data['nazev']
        if not nazev or len(nazev.strip()) < 2:
            raise forms.ValidationError('Název akcie musí být zadán a mít alespoň 2 znaky.')
        return nazev.strip()

    def clean(self):
        cleaned = super().clean()
        if cleaned.get('hodnota') is not None and cleaned.get('nakup') is not None:
            from decimal import Decimal
            if cleaned['hodnota'] < cleaned['nakup'] * Decimal('0.5'):
                self.add_error('hodnota', 'Hodnota je podezřele nízká vůči nákupu. Zkontrolujte zadání.')
        return cleaned

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
    castka = forms.DecimalField(label='Částka', max_digits=10, decimal_places=2, min_value=0, error_messages={'min_value': 'Dividenda musí být nezáporná.'})
    class Meta:
        model = Dividenda
        fields = ['akcie', 'datum', 'castka']

    def clean_castka(self):
        castka = self.cleaned_data['castka']
        if castka > 1000000:
            raise forms.ValidationError('Dividenda je příliš vysoká. Zkontrolujte zadání.')
        return castka

class CustomUserForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'receive_monthly_reports', 'email_for_reports')

class KlientForm(forms.ModelForm):
    class Meta:
        model = Klient
        fields = ['jmeno', 'prijmeni', 'email', 'telefon', 'adresa', 'poznamka', 'poradce']

class PortfolioForm(forms.ModelForm):
    class Meta:
        model = Portfolio
        fields = ['nazev', 'popis', 'klient']