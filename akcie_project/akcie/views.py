import csv
import openpyxl
from openpyxl.styles import Font
from django.http import HttpResponse, FileResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q, Sum, Count
from django.db.models.functions import TruncMonth
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
from django.contrib.auth.decorators import login_required
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from io import BytesIO
from django.urls import reverse
from django.core.mail import EmailMessage
from django.utils.timezone import now
import os
from .models import Akcie, Transakce, Dividenda, Aktivita, CustomUser
from .forms import AkcieForm, TransakceForm, DividendaForm, CustomUserForm

def log_aktivita(akce, uzivatel=None):
    Aktivita.objects.create(akce=akce, uzivatel=uzivatel)

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
    akcie = get_object_or_404(Akcie, pk=pk)
    transakce = Transakce.objects.filter(akcie=akcie)
    dividendy = Dividenda.objects.filter(akcie=akcie)

    total_dividendy = dividendy.aggregate(Sum('castka'))['castka__sum'] or 0

    context = {
        'akcie': akcie,
        'transakce': transakce,
        'dividendy': dividendy,
        'total_dividendy': total_dividendy,
    }
    return render(request, 'akcie/akcie_detail.html', context)

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

def import_excel(request):
    if request.method == 'POST' and request.FILES['excel_file']:
        excel_file = request.FILES['excel_file']
        wb = openpyxl.load_workbook(excel_file)
        sheet = wb.active

        for row in sheet.iter_rows(min_row=2, values_only=True):
            Akcie.objects.create(
                nazev=row[0],
                pocet_ks=row[1],
                cena_za_kus=row[2],
                hodnota=row[3],
                nakup=row[4],
                zisk_ztrata=row[5],
                dividenda=row[6]
            )

        log_aktivita("Import dat z Excelu", request.user.username if request.user.is_authenticated else "Anonymní")

        return redirect('akcie_list')

    return render(request, 'akcie/import_form.html')

def export_excel(request):
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="akcie_export.xlsx"'

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Akcie"

    # Přidání záhlaví
    headers = ["Název", "Počet kusů", "Cena za kus", "Hodnota", "Nákup", "Zisk/Ztráta", "Dividenda"]
    ws.append(headers)

    for cell in ws[1]:
        cell.font = Font(bold=True)

    # Přidání dat
    for akcie in Akcie.objects.all():
        ws.append([
            akcie.nazev,
            akcie.pocet_ks,
            akcie.cena_za_kus,
            akcie.hodnota,
            akcie.nakup,
            akcie.zisk_ztrata,
            akcie.dividenda
        ])

    log_aktivita("Export dat do Excelu", request.user.username if request.user.is_authenticated else "Anonymní")

    wb.save(response)
    return response

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

def export_dashboard_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="dashboard_report.pdf"'

    p = canvas.Canvas(response, pagesize=letter)
    p.setFont("Helvetica", 12)

    p.drawString(100, 750, "Dashboard Report")

    total_akcie = Akcie.objects.count()
    total_transakce = Transakce.objects.count()
    total_dividendy = Dividenda.objects.aggregate(Sum('castka'))['castka__sum'] or 0

    p.drawString(100, 700, f"Počet akcií: {total_akcie}")
    p.drawString(100, 680, f"Počet transakcí: {total_transakce}")
    p.drawString(100, 660, f"Celková částka dividend: {total_dividendy} Kč")

    p.showPage()
    p.save()
    return response

def export_dashboard_graphs_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="dashboard_graphs.pdf"'

    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    p.setFont("Helvetica", 12)

    p.drawString(100, 750, "Dashboard Grafy")

    # Screenshot grafů pomocí Selenium
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        driver.get(request.build_absolute_uri(reverse('dashboard')))
        driver.set_window_size(1200, 800)
        screenshot = driver.get_screenshot_as_png()
        image = ImageReader(BytesIO(screenshot))
        p.drawImage(image, 50, 400, width=500, height=300)
    finally:
        driver.quit()

    p.showPage()
    p.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='dashboard_graphs.pdf')

def dashboard(request):
    query = request.GET.get('q')

    if query:
        akcie = Akcie.objects.filter(Q(nazev__icontains=query))
    else:
        akcie = Akcie.objects.all()

    total_akcie = akcie.count()
    total_hodnota = akcie.aggregate(Sum('hodnota'))['hodnota__sum'] or 0
    total_zisk_ztrata = akcie.aggregate(Sum('zisk_ztrata'))['zisk_ztrata__sum'] or 0

    akcie_data = akcie.values('nazev', 'hodnota')

    transakce_monthly = (
        Transakce.objects.annotate(month=TruncMonth('datum'))
        .values('month')
        .annotate(count=Count('id'))
        .order_by('month')
    )

    dividendy_data = (
        Dividenda.objects.values('akcie__nazev')
        .annotate(total_castka=Sum('castka'))
        .order_by('akcie__nazev')
    )

    current_year = now().year
    months = ["Leden", "Únor", "Březen", "Duben", "Květen", "Červen", "Červenec", "Srpen", "Září", "Říjen", "Listopad", "Prosinec"]
    investment_data = []

    for month in range(1, 13):
        total_investment = Transakce.objects.filter(date__year=current_year, date__month=month).aggregate(Sum('amount'))['amount__sum'] or 0
        investment_data.append(total_investment)

    context = {
        'total_akcie': total_akcie,
        'total_hodnota': total_hodnota,
        'total_zisk_ztrata': total_zisk_ztrata,
        'akcie_data': list(akcie_data),
        'transakce_monthly': list(transakce_monthly),
        'dividendy_data': list(dividendy_data),
        'months': months,
        'investment_data': investment_data,
        'query': query,
    }
    return render(request, 'akcie/dashboard.html', context)

def aktivity_list(request):
    query_user = request.GET.get('user')
    query_action = request.GET.get('action')

    aktivity = Aktivita.objects.all()

    if query_user:
        aktivity = aktivity.filter(uzivatel__icontains=query_user)
    if query_action:
        aktivity = aktivity.filter(akce__icontains=query_action)

    aktivity = aktivity.order_by('-datum_cas')

    return render(request, 'akcie/aktivity_list.html', {
        'aktivity': aktivity,
        'query_user': query_user,
        'query_action': query_action
    })

def export_aktivity_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="aktivity.csv"'

    writer = csv.writer(response)
    writer.writerow(['Akce', 'Uživatel', 'Datum a čas'])

    for aktivita in Aktivita.objects.all():
        writer.writerow([aktivita.akce, aktivita.uzivatel, aktivita.datum_cas])

    return response

def export_aktivity_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="aktivity_report.pdf"'

    p = canvas.Canvas(response, pagesize=letter)
    p.setFont("Helvetica", 12)

    p.drawString(100, 750, "Seznam aktivit")

    y = 720
    for aktivita in Aktivita.objects.all():
        p.drawString(100, y, f"Akce: {aktivita.akce}, Uživatel: {aktivita.uzivatel}, Datum a čas: {aktivita.datum_cas}")
        y -= 20
        if y < 50:
            p.showPage()
            p.setFont("Helvetica", 12)
            y = 750

    p.save()
    return response

def send_monthly_report():
    users = CustomUser.objects.filter(receive_monthly_reports=True)
    pdf_path = generate_pdf_report()  # Generování PDF reportu
    for user in users:
        subject = "Měsíční report investic"
        body = f"Dobrý den, {user.username},\n\nPřikládáme měsíční report vašich investic."
        email = EmailMessage(
            subject,
            body,
            'your_email@gmail.com',  # Odesílatel
            [user.email_for_reports]  # Příjemce
        )

        email.attach_file(pdf_path)
        email.send()

def generate_pdf_report():
    pdf_path = os.path.join('staticfiles', 'reports', 'monthly_report.pdf')
    os.makedirs(os.path.dirname(pdf_path), exist_ok=True)
    c = canvas.Canvas(pdf_path)
    c.drawString(100, 750, "Měsíční report investic")
    c.drawString(100, 730, "Tento report obsahuje souhrn vašich investic za poslední měsíc.")
    c.save()
    return pdf_path

@login_required
def user_preferences(request):
    if request.method == 'POST':
        form = CustomUserForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = CustomUserForm(instance=request.user)
    return render(request, 'akcie/user_preferences.html', {'form': form})
