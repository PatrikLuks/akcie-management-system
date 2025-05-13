# Akcie Management System

## Popis projektu
Tento projekt je webová aplikace pro správu investic do akcií. Umožňuje uživatelům provádět CRUD operace, import/export dat, generovat reporty ve formátu PDF, vizualizovat data pomocí grafů a spravovat uživatelské preference. Aplikace také podporuje plánované úlohy pro měsíční generování reportů a jejich odesílání e-mailem.

## Funkce
- CRUD operace pro akcie, transakce a dividendy.
- Import a export dat ve formátu CSV a Excel.
- Generování reportů ve formátu PDF.
- Dashboard s vizualizacemi pomocí Chart.js.
- Uživatelská autentizace a správa preferencí.
- Plánované úlohy pro měsíční reporty a e-maily.

## Nové funkce

### Export dat do JSON
- Data o akciích lze exportovat do JSON formátu na URL:
  ```
  /akcie/export_json/
  ```

### Filtrování a třídění na dashboardu
- Uživatelé mohou filtrovat a třídit data přímo na dashboardu pomocí interaktivních prvků.

### Automatické zálohování databáze
- Cron úloha automaticky zálohuje databázi jednou denně do adresáře `backups`.
- Pro ruční spuštění cron úloh:
  ```bash
  python manage.py runcrons
  ```

### Export všech dat do ZIP
- Všechna data (akcie, transakce, dividendy) lze exportovat do jednoho ZIP souboru na URL:
  ```
  /export_all_data_zip/
  ```

### Notifikace pro uživatele
- Uživatelé obdrží vizuální oznámení při úspěšném exportu nebo jiných akcích.

### Automatické čištění starých záloh
- Cron úloha automaticky odstraňuje zálohy starší než 7 dní z adresáře `backups`.
- Pro ruční spuštění cron úloh:
  ```bash
  python manage.py runcrons
  ```

## Požadavky
- Python 3.9+
- Django 4.0+
- Další závislosti uvedené v `requirements.txt`.

## Instalace
1. Klonujte repozitář:
   ```bash
   git clone https://github.com/PatrikLuks/akcie-management-system.git
   ```
2. Přesuňte se do adresáře projektu:
   ```bash
   cd akcie-management-system/akcie_project
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
5. Proveďte migrace databáze:
   ```bash
   python manage.py migrate
   ```
6. Vytvořte superuživatele:
   ```bash
   python manage.py createsuperuser
   ```
7. Spusťte vývojový server:
   ```bash
   python manage.py runserver
   ```

## Použití
- Přihlaste se do administrace na `http://127.0.0.1:8000/admin`.
- Používejte dashboard a další funkce aplikace na `http://127.0.0.1:8000/`.

## Plánované úlohy
- Plánované úlohy jsou spravovány pomocí `django-cron`.
- Pro ruční spuštění cron úloh použijte:
  ```bash
  python manage.py runcrons
  ```

## Testování

1. Spuštění testů:
   ```bash
   python manage.py test
   ```
   - Testy pokrývají CRUD operace, dashboard a další klíčové funkce.

2. Ověření plánovaných úloh:
   - Spusťte cron úlohy ručně:
     ```bash
     python manage.py runcrons
     ```

## Nasazení

1. Nastavte proměnné prostředí:
   - `DJANGO_SECRET_KEY`: Tajný klíč pro aplikaci.

2. Změňte `DEBUG` na `False` v `settings.py` pro produkční prostředí.

3. Použijte `gunicorn` nebo jiný WSGI server pro nasazení:
   ```bash
   gunicorn akcie_project.wsgi:application
   ```

4. Konfigurujte statické soubory:
   ```bash
   python manage.py collectstatic
   ```

## Automatizace nasazení

1. Ujistěte se, že máte nastavené virtuální prostředí a nainstalované závislosti.
2. Spusťte skript pro nasazení:
   ```bash
   bash deploy.sh
   ```
3. Skript provede následující kroky:
   - Aktivuje virtuální prostředí.
   - Provede migrace databáze.
   - Nasbírá statické soubory.
   - Spustí server na adrese `0.0.0.0:8000`.

## Logování a zálohování

1. Skript `deploy.sh` nyní automaticky:
   - Zálohuje databázi do adresáře `backups` s časovým razítkem.
   - Zaznamenává všechny kroky nasazení do souboru `deploy.log`.

2. Pro zobrazení logu nasazení:
   ```bash
   cat deploy.log
   ```

3. Pro obnovení databáze ze zálohy:
   - Najděte požadovanou zálohu v adresáři `backups`.
   - Nahraďte aktuální databázi příslušným souborem:
     ```bash
     cp backups/db_backup_<datum>.sqlite3 akcie_project/db.sqlite3
     ```

## Autor
Patrik Luks

## Licence
Tento projekt je licencován pod MIT licencí.
