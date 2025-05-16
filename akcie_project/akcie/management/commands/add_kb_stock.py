from django.core.management.base import BaseCommand
from akcie.models import Akcie, Dividenda, get_user_model
from django.utils.timezone import now
from decimal import Decimal

class Command(BaseCommand):
    help = 'Přidá akcii KOMERCNI BANKA a související dividendu, pokud ještě neexistuje.'

    def handle(self, *args, **options):
        User = get_user_model()
        user = User.objects.first()
        if not user:
            self.stdout.write(self.style.ERROR('V databázi není žádný uživatel. Nejprve vytvořte uživatele.'))
            return

        akcie_qs = Akcie.objects.filter(nazev='KOMERCNI BANKA')
        if akcie_qs.exists():
            akcie = akcie_qs.first()
            self.stdout.write('Akcie KOMERCNI BANKA již existuje (používám první nalezenou).')
        else:
            akcie = Akcie.objects.create(
                user=user,
                nazev='KOMERCNI BANKA',
                datum=now().date(),
                cas=now().time(),
                pocet_ks=10,
                cena_za_kus=Decimal('800.00'),
                hodnota=Decimal('8000.00'),
                nakup=Decimal('8000.00'),
                zisk_ztrata=Decimal('0.00'),
                ticker='KOMB.PR',
                mena='CZK',
            )
            self.stdout.write(self.style.SUCCESS('Akcie KOMERCNI BANKA byla vytvořena.'))

        # Přidání dividendy
        dividenda, div_created = Dividenda.objects.get_or_create(
            akcie=akcie,
            datum=now().date(),
            defaults={
                'castka': Decimal('500.00'),
            }
        )
        if div_created:
            self.stdout.write(self.style.SUCCESS('Dividenda pro KOMERCNI BANKA byla vytvořena.'))
        else:
            self.stdout.write('Dividenda pro KOMERCNI BANKA již existuje pro dnešní datum.')
