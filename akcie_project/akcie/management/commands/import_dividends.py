from django.core.management.base import BaseCommand
from akcie.models import Akcie, Dividenda
from django.utils.timezone import make_aware
from decimal import Decimal
import yfinance as yf
from datetime import datetime

class Command(BaseCommand):
    help = 'Načte a uloží reálné dividendy z trhu pro všechny akcie s tickerem.'

    def handle(self, *args, **options):
        akcie_qs = Akcie.objects.exclude(ticker__isnull=True).exclude(ticker='')
        total_new = 0
        for akcie in akcie_qs:
            ticker = akcie.ticker
            self.stdout.write(f'Zpracovávám {akcie.nazev} ({ticker})...')
            try:
                stock = yf.Ticker(ticker)
                dividends = stock.dividends
                if dividends.empty:
                    self.stdout.write('  Žádné dividendy nenalezeny.')
                    continue
                for date, amount in dividends.items():
                    datum = make_aware(datetime.combine(date, datetime.min.time()))
                    # Ověř, zda už dividenda pro tento den existuje
                    if not Dividenda.objects.filter(akcie=akcie, datum=datum.date()).exists():
                        Dividenda.objects.create(
                            akcie=akcie,
                            datum=datum.date(),
                            castka=Decimal(str(amount))
                        )
                        total_new += 1
                        self.stdout.write(self.style.SUCCESS(f'  Přidána dividenda {datum.date()} - {amount}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'  Chyba: {e}'))
        self.stdout.write(self.style.SUCCESS(f'Hotovo. Přidáno {total_new} nových dividend.'))
