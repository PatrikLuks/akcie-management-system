# Akcie Management System

Tento projekt je webová aplikace postavená na frameworku Django, která umožňuje správu investic do akcií, transakcí a dividend.

## Funkcionality
- Přidávání, úprava a mazání záznamů akcií, transakcí a dividend.
- Zobrazení seznamů a detailů jednotlivých záznamů.
- Navigace mezi stránkami.
- Validace formulářů a základní stylování pomocí CSS.

## Požadavky
- Python 3.9 nebo novější
- Django 4.2

## Instalace
1. Naklonujte tento repozitář:
   ```bash
   git clone <URL_REPOZITÁŘE>
   ```
2. Přesuňte se do adresáře projektu:
   ```bash
   cd akcie_project
   ```
3. Vytvořte a aktivujte virtuální prostředí:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
4. Nainstalujte závislosti:
   ```bash
   pip install -r requirements.txt
   ```

## Spuštění
1. Proveďte migrace databáze:
   ```bash
   python manage.py migrate
   ```
2. Spusťte vývojový server:
   ```bash
   python manage.py runserver
   ```
3. Otevřete aplikaci v prohlížeči na adrese [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

## Struktura projektu
- `akcie/` - Aplikace obsahující modely, pohledy, šablony a statické soubory.
- `akcie_project/` - Hlavní nastavení projektu Django.
- `static/` - Statické soubory (CSS, JavaScript, obrázky).
- `templates/` - HTML šablony.

## Autor
Patrik Luks

## Licence
Tento projekt je licencován pod licencí MIT.
