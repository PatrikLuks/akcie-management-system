from django.test import TestCase
from .models import Akcie, Transakce, Dividenda, CustomUser
from django.utils.timezone import now
from django.urls import reverse
from .forms import AkcieForm

class AkcieModelTest(TestCase):
    def setUp(self):
        self.akcie = Akcie.objects.create(
            nazev="Testovací akcie",
            pocet_ks=100,
            cena_za_kus=150.50,
            hodnota=15050.00,
            nakup=14000.00,
            zisk_ztrata=1050.00,
            dividenda=500.00
        )

    def test_akcie_str(self):
        self.assertEqual(str(self.akcie), "Testovací akcie")

class TransakceModelTest(TestCase):
    def setUp(self):
        self.akcie = Akcie.objects.create(
            nazev="Testovací akcie",
            pocet_ks=100,
            cena_za_kus=150.50,
            hodnota=15050.00,
            nakup=14000.00,
            zisk_ztrata=1050.00,
            dividenda=500.00
        )
        self.transakce = Transakce.objects.create(
            akcie=self.akcie,
            datum=now().date(),
            typ="nákup",
            mnozstvi=50,
            cena=7500.00
        )

    def test_transakce_str(self):
        self.assertEqual(str(self.transakce), "nákup - Testovací akcie")

class DividendaModelTest(TestCase):
    def setUp(self):
        self.akcie = Akcie.objects.create(
            nazev="Testovací akcie",
            pocet_ks=100,
            cena_za_kus=150.50,
            hodnota=15050.00,
            nakup=14000.00,
            zisk_ztrata=1050.00,
            dividenda=500.00
        )
        self.dividenda = Dividenda.objects.create(
            akcie=self.akcie,
            datum=now().date(),
            castka=500.00
        )

    def test_dividenda_str(self):
        self.assertEqual(str(self.dividenda), "Dividenda - Testovací akcie")

class AkcieViewTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.akcie = Akcie.objects.create(
            nazev="Testovací akcie",
            pocet_ks=100,
            cena_za_kus=150.50,
            hodnota=15050.00,
            nakup=14000.00,
            zisk_ztrata=1050.00,
            dividenda=500.00
        )

    def test_akcie_list_view(self):
        response = self.client.get(reverse('akcie_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Testovací akcie")
        self.assertTemplateUsed(response, 'akcie/akcie_list.html')

    def test_akcie_detail_view(self):
        response = self.client.get(reverse('akcie_detail', args=[self.akcie.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Testovací akcie")
        self.assertTemplateUsed(response, 'akcie/akcie_detail.html')

class AkcieFormTest(TestCase):
    def test_valid_form(self):
        data = {
            'nazev': 'Testovací akcie',
            'pocet_ks': 100,
            'cena_za_kus': 150.50,
            'hodnota': 15050.00,
            'nakup': 14000.00,
            'zisk_ztrata': 1050.00,
            'dividenda': 500.00
        }
        form = AkcieForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        data = {
            'nazev': '',  # Název je povinný
            'pocet_ks': -10,  # Počet kusů nemůže být záporný
            'cena_za_kus': 150.50,
            'hodnota': 15050.00,
            'nakup': 14000.00,
            'zisk_ztrata': 1050.00,
            'dividenda': 500.00
        }
        form = AkcieForm(data=data)
        self.assertFalse(form.is_valid())

class PDFGenerationTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.akcie = Akcie.objects.create(
            nazev="Testovací akcie",
            pocet_ks=100,
            cena_za_kus=150.50,
            hodnota=15050.00,
            nakup=14000.00,
            zisk_ztrata=1050.00,
            dividenda=500.00
        )

    def test_generate_akcie_pdf(self):
        response = self.client.get(reverse('generate_akcie_pdf'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/pdf")

class AuthenticationTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='testuser', password='testpassword')

    def test_login_required(self):
        response = self.client.get(reverse('akcie_list'))
        self.assertNotEqual(response.status_code, 200)
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('akcie_list'))
        self.assertEqual(response.status_code, 200)

class AkcieCRUDTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.akcie = Akcie.objects.create(
            nazev="Testovací akcie",
            pocet_ks=100,
            cena_za_kus=150.50,
            hodnota=15050.00,
            nakup=14000.00,
            zisk_ztrata=1050.00,
            dividenda=500.00
        )

    def test_akcie_create(self):
        response = self.client.post(reverse('akcie_create'), {
            'nazev': 'Nová akcie',
            'pocet_ks': 50,
            'cena_za_kus': 200.00,
            'hodnota': 10000.00,
            'nakup': 9000.00,
            'zisk_ztrata': 1000.00,
            'dividenda': 300.00
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Akcie.objects.last().nazev, 'Nová akcie')

    def test_akcie_list_view(self):
        response = self.client.get(reverse('akcie_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Testovací akcie')

    def test_akcie_detail_view(self):
        response = self.client.get(reverse('akcie_detail', args=[self.akcie.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Testovací akcie')

    def test_akcie_update(self):
        response = self.client.post(reverse('akcie_update', args=[self.akcie.id]), {
            'nazev': 'Aktualizovaná akcie',
            'pocet_ks': 150,
            'cena_za_kus': 160.00,
            'hodnota': 24000.00,
            'nakup': 20000.00,
            'zisk_ztrata': 4000.00,
            'dividenda': 800.00
        })
        self.assertEqual(response.status_code, 302)
        self.akcie.refresh_from_db()
        self.assertEqual(self.akcie.nazev, 'Aktualizovaná akcie')

    def test_akcie_delete(self):
        response = self.client.post(reverse('akcie_delete', args=[self.akcie.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Akcie.objects.filter(id=self.akcie.id).exists())
