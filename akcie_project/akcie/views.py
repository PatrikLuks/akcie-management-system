from django.shortcuts import render, redirect, get_object_or_404
from .models import Akcie, Transakce, Dividenda
from .forms import AkcieForm, TransakceForm, DividendaForm

def index(request):
    return render(request, 'akcie/index.html')

def akcie_list(request):
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

def transakce_list(request):
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

def dividenda_list(request):
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
