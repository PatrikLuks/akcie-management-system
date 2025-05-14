from django.test import TestCase
from .models import Akcie, Transakce, Dividenda, CustomUser
from django.utils.timezone import now
from django.urls import reverse
from .forms import AkcieForm
from unittest.mock import patch
from .views import fetch_akcie_data, fetch_hot_investments
import yfinance as yf
from datetime import date

class AkcieModelTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='testuser', password='testpassword')
        self.akcie = Akcie.objects.create(
            nazev="Testovací akcie",
            pocet_ks=100,
            cena_za_kus=150.50,
            hodnota=15050.00,
            nakup=14000.00,
            zisk_ztrata=1050.00,
            dividenda=500.00,
            user=self.user
        )

    def test_akcie_str(self):
        self.assertEqual(str(self.akcie), "Testovací akcie")

class TransakceModelTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='testuser', password='testpassword')
        self.akcie = Akcie.objects.create(
            nazev="Testovací akcie",
            pocet_ks=100,
            cena_za_kus=150.50,
            hodnota=15050.00,
            nakup=14000.00,
            zisk_ztrata=1050.00,
            dividenda=500.00,
            user=self.user
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
        self.user = CustomUser.objects.create_user(username='testuser', password='testpassword')
        self.akcie = Akcie.objects.create(
            nazev="Testovací akcie",
            pocet_ks=100,
            cena_za_kus=150.50,
            hodnota=15050.00,
            nakup=14000.00,
            zisk_ztrata=1050.00,
            dividenda=500.00,
            user=self.user
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
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='formuser', password='testpassword')

    def test_valid_form(self):
        data = {
            'nazev': 'Testovací akcie',
            'pocet_ks': 100,
            'cena_za_kus': 150.50,
            'hodnota': 15050.00,
            'nakup': 14000.00,
            'zisk_ztrata': 1050.00,
            'dividenda': 500.00,
            'datum': now().date(),
            'cas': now().time()
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
            'dividenda': 500.00,
            'datum': now().date(),
            'cas': now().time()
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
            dividenda=500.00,
            user=self.user,
            datum=now().date(),
            cas=now().time()
        )

    def test_akcie_create(self):
        response = self.client.post(reverse('akcie_create'), {
            'nazev': 'Nová akcie',
            'pocet_ks': 50,
            'cena_za_kus': 200.00,
            'hodnota': 10000.00,
            'nakup': 9000.00,
            'zisk_ztrata': 1000.00,
            'dividenda': 300.00,
            'datum': now().date(),
            'cas': now().time()
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
            'dividenda': 800.00,
            'datum': now().date(),
            'cas': now().time()
        })
        self.assertEqual(response.status_code, 302)
        self.akcie.refresh_from_db()
        self.assertEqual(self.akcie.nazev, 'Aktualizovaná akcie')

    def test_akcie_delete(self):
        response = self.client.post(reverse('akcie_delete', args=[self.akcie.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Akcie.objects.filter(id=self.akcie.id).exists())

class APITest(TestCase):
    @patch('requests.get')
    def test_fetch_akcie_data_success(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = [{'name': 'Stock A'}, {'name': 'Stock B'}]

        data = fetch_akcie_data()
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['name'], 'Stock A')

    @patch('requests.get')
    def test_fetch_akcie_data_failure(self, mock_get):
        mock_get.return_value.status_code = 500

        data = fetch_akcie_data()
        self.assertEqual(data, [])

    @patch('akcie.views.yf.Ticker')
    def test_fetch_hot_investments_success(self, mock_ticker):
        mock_ticker.return_value.info = {
            'shortName': 'Apple Inc.',
            'regularMarketPrice': 212.31,
            'marketCap': 3171094364160
        }

        data = fetch_hot_investments()
        self.assertEqual(len(data), 10)
        self.assertEqual(data[0]['nazev'], 'Apple Inc.')

    @patch('akcie.views.yf.Ticker')
    def test_fetch_hot_investments_failure(self, mock_ticker):
        mock_ticker.side_effect = Exception("API Error")

        data = fetch_hot_investments()
        self.assertEqual(data, [])

class AkcieZiskZtrataTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='ziskuser', password='testpassword')

    @patch('yfinance.Ticker')
    def test_zisk_ztrata_vypocet(self, mock_ticker):
        # Simulace historické a aktuální ceny
        mock_ticker.return_value.history.side_effect = [
            # Historická cena v den nákupu
            {'Close': [100]},
            # Aktuální cena
            {'Close': [150]}
        ]
        mock_ticker.return_value.info = {'regularMarketPrice': 150}

        # Vytvoření akcie s datem nákupu v minulosti
        akcie = Akcie(
            nazev="Testovací akcie",
            pocet_ks=10,
            cena_za_kus=100,
            hodnota=1000,
            nakup=1000,
            zisk_ztrata=0,
            dividenda=0,
            user=self.user
        )
        # Simulace výpočtu zisku/ztráty
        purchase_price = 100
        current_price = 150
        akcie.zisk_ztrata = (current_price - purchase_price) * akcie.pocet_ks
        akcie.save()
        self.assertEqual(akcie.zisk_ztrata, 500)
