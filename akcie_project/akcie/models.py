from django.db import models

class Akcie(models.Model):
    nazev = models.CharField(max_length=100)
    pocet_ks = models.IntegerField()
    cena_za_kus = models.DecimalField(max_digits=10, decimal_places=2)
    hodnota = models.DecimalField(max_digits=15, decimal_places=2)
    nakup = models.DecimalField(max_digits=15, decimal_places=2)
    zisk_ztrata = models.DecimalField(max_digits=15, decimal_places=2)
    dividenda = models.DecimalField(max_digits=15, decimal_places=2)

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
