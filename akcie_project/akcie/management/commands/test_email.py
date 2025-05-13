from django.core.mail import send_mail
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Test email configuration'

    def handle(self, *args, **kwargs):
        send_mail(
            'Testovací e-mail',
            'Toto je testovací e-mail pro ověření konfigurace.',
            'your_email@gmail.com',  # Odesílatel
            ['recipient_email@gmail.com'],  # Příjemce
            fail_silently=False,
        )
        self.stdout.write(self.style.SUCCESS('Testovací e-mail byl úspěšně odeslán.'))