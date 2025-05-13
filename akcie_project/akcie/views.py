import csv
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from reportlab.pdfgen import canvas
from django.contrib.auth.decorators import login_required
from .models import Akcie, Transakce, Dividenda
from .forms import AkcieForm, TransakceForm, DividendaForm

def index(request):
    return render(request, 'akcie/index.html')

@login_required
def akcie_list(request):
    query = request.GET.get('q')
    if query:
        akcie = Akcie.objects.filter(
            Q(nazev__icontains=query) |
            Q(pocet_ks__icontains=query) |
            Q(cena_za_kus__icontains=query)
        )
    else:
        akcie = Akcie.objects.all()
    return render(request, 'akcie/akcie_list.html', {'akcie': akcie})

def akcie_detail(request, pk):
    akcie = Akcie.objects.get(pk=pk)
    return render(request, 'akcie/akcie_detail.html', {'akcie': akcie})

def akcie_create(request):
    if request.method == 'POST':
        form = AkcieForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('akcie_list')
    else:
        form = AkcieForm()
    return render(request, 'akcie/akcie_form.html', {'form': form})

def akcie_update(request, pk):
    akcie = get_object_or_404(Akcie, pk=pk)
    if request.method == 'POST':
        form = AkcieForm(request.POST, instance=akcie)
        if form.is_valid():
            form.save()
            return redirect('akcie_list')
    else:
        form = AkcieForm(instance=akcie)
    return render(request, 'akcie/akcie_form.html', {'form': form})

def akcie_delete(request, pk):
    akcie = get_object_or_404(Akcie, pk=pk)
    if request.method == 'POST':
        akcie.delete()
        return redirect('akcie_list')
    return render(request, 'akcie/akcie_confirm_delete.html', {'akcie': akcie})

@login_required
def transakce_list(request):
    query = request.GET.get('q')
    if query:
        transakce = Transakce.objects.filter(
            Q(akcie__nazev__icontains=query) |
            Q(typ__icontains=query) |
            Q(mnozstvi__icontains=query) |
            Q(cena__icontains=query)
        )
    else:
        transakce = Transakce.objects.all()
    return render(request, 'akcie/transakce_list.html', {'transakce': transakce})

def transakce_detail(request, pk):
    transakce = Transakce.objects.get(pk=pk)
    return render(request, 'akcie/transakce_detail.html', {'transakce': transakce})

def transakce_create(request):
    if request.method == 'POST':
        form = TransakceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('transakce_list')
    else:
        form = TransakceForm()
    return render(request, 'akcie/transakce_form.html', {'form': form})

def transakce_update(request, pk):
    transakce = get_object_or_404(Transakce, pk=pk)
    if request.method == 'POST':
        form = TransakceForm(request.POST, instance=transakce)
        if form.is_valid():
            form.save()
            return redirect('transakce_list')
    else:
        form = TransakceForm(instance=transakce)
    return render(request, 'akcie/transakce_form.html', {'form': form})

def transakce_delete(request, pk):
    transakce = get_object_or_404(Transakce, pk=pk)
    if request.method == 'POST':
        transakce.delete()
        return redirect('transakce_list')
    return render(request, 'akcie/transakce_confirm_delete.html', {'transakce': transakce})

@login_required
def dividenda_list(request):
    query = request.GET.get('q')
    if query:
        dividendy = Dividenda.objects.filter(
            Q(akcie__nazev__icontains=query) |
            Q(castka__icontains=query)
        )
    else:
        dividendy = Dividenda.objects.all()
    return render(request, 'akcie/dividenda_list.html', {'dividendy': dividendy})

def dividenda_detail(request, pk):
    dividenda = Dividenda.objects.get(pk=pk)
    return render(request, 'akcie/dividenda_detail.html', {'dividenda': dividenda})

def dividenda_create(request):
    if request.method == 'POST':
        form = DividendaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dividenda_list')
    else:
        form = DividendaForm()
    return render(request, 'akcie/dividenda_form.html', {'form': form})

def dividenda_update(request, pk):
    dividenda = get_object_or_404(Dividenda, pk=pk)
    if request.method == 'POST':
        form = DividendaForm(request.POST, instance=dividenda)
        if form.is_valid():
            form.save()
            return redirect('dividenda_list')
    else:
        form = DividendaForm(instance=dividenda)
    return render(request, 'akcie/dividenda_form.html', {'form': form})

def dividenda_delete(request, pk):
    dividenda = get_object_or_404(Dividenda, pk=pk)
    if request.method == 'POST':
        dividenda.delete()
        return redirect('dividenda_list')
    return render(request, 'akcie/dividenda_confirm_delete.html', {'dividenda': dividenda})

def export_akcie_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="akcie.csv"'

    writer = csv.writer(response)
    writer.writerow(['Název', 'Počet kusů', 'Cena za kus', 'Hodnota', 'Nákup', 'Zisk/Ztráta', 'Dividenda'])

    akcie = Akcie.objects.all()
    for a in akcie:
        writer.writerow([a.nazev, a.pocet_ks, a.cena_za_kus, a.hodnota, a.nakup, a.zisk_ztrata, a.dividenda])

    return response

def export_transakce_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="transakce.csv"'

    writer = csv.writer(response)
    writer.writerow(['Akcie', 'Datum', 'Typ', 'Množství', 'Cena'])

    transakce = Transakce.objects.all()
    for t in transakce:
        writer.writerow([t.akcie.nazev, t.datum, t.typ, t.mnozstvi, t.cena])

    return response

def export_dividendy_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="dividendy.csv"'

    writer = csv.writer(response)
    writer.writerow(['Akcie', 'Datum', 'Částka'])

    dividendy = Dividenda.objects.all()
    for d in dividendy:
        writer.writerow([d.akcie.nazev, d.datum, d.castka])

    return response

def import_akcie_csv(request):
    if request.method == 'POST' and request.FILES['csv_file']:
        csv_file = request.FILES['csv_file']
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'Soubor musí být ve formátu CSV.')
            return render(request, 'akcie/import_form.html')

        decoded_file = csv_file.read().decode('utf-8').splitlines()
        reader = csv.reader(decoded_file)
        next(reader)  # Přeskočit hlavičku
        for row in reader:
            Akcie.objects.create(
                nazev=row[0],
                pocet_ks=int(row[1]),
                cena_za_kus=float(row[2]),
                hodnota=float(row[3]),
                nakup=float(row[4]),
                zisk_ztrata=float(row[5]),
                dividenda=float(row[6])
            )
        messages.success(request, 'Data byla úspěšně importována.')
        return render(request, 'akcie/import_form.html')

    return render(request, 'akcie/import_form.html')

def generate_akcie_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="akcie_report.pdf"'

    p = canvas.Canvas(response)
    p.setFont("Helvetica", 12)

    p.drawString(100, 800, "Report o akciích")
    y = 780

    akcie = Akcie.objects.all()
    for a in akcie:
        p.drawString(100, y, f"Název: {a.nazev}, Počet kusů: {a.pocet_ks}, Cena za kus: {a.cena_za_kus}")
        y -= 20

    p.showPage()
    p.save()
    return response

def generate_transakce_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="transakce_report.pdf"'

    p = canvas.Canvas(response)
    p.setFont("Helvetica", 12)

    p.drawString(100, 800, "Report o transakcích")
    y = 780

    transakce = Transakce.objects.all()
    for t in transakce:
        p.drawString(100, y, f"Akcie: {t.akcie.nazev}, Typ: {t.typ}, Množství: {t.mnozstvi}, Cena: {t.cena}")
        y -= 20

    p.showPage()
    p.save()
    return response

def generate_dividenda_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="dividenda_report.pdf"'

    p = canvas.Canvas(response)
    p.setFont("Helvetica", 12)

    p.drawString(100, 800, "Report o dividendách")
    y = 780

    dividendy = Dividenda.objects.all()
    for d in dividendy:
        p.drawString(100, y, f"Akcie: {d.akcie.nazev}, Částka: {d.castka}, Datum: {d.datum}")
        y -= 20

    p.showPage()
    p.save()
    return response
