import os
import time
from django_cron import CronJobBase, Schedule
from django.utils.timezone import now
from .views import export_dashboard_graphs_pdf, send_monthly_report

class MonthlyReportCronJob(CronJobBase):
    RUN_EVERY_MINS = 43200  # Spouští se jednou za měsíc (30 dní)

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'akcie.monthly_report_cron_job'

    def do(self):
        send_monthly_report()

class BackupDatabaseCronJob(CronJobBase):
    RUN_EVERY_MINS = 1440  # Spuštění jednou denně

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'akcie.backup_database_cron_job'

    def do(self):
        backup_dir = 'backups'
        os.makedirs(backup_dir, exist_ok=True)
        timestamp = now().strftime('%Y-%m-%d_%H-%M-%S')
        backup_file = os.path.join(backup_dir, f'db_backup_{timestamp}.sqlite3')
        if os.path.exists('db.sqlite3'):
            with open('db.sqlite3', 'rb') as src, open(backup_file, 'wb') as dst:
                dst.write(src.read())
            print(f'Záloha databáze byla vytvořena: {backup_file}')
        else:
            print('Databáze nebyla nalezena, záloha nebyla vytvořena.')

class CleanOldBackupsCronJob(CronJobBase):
    RUN_EVERY_MINS = 1440  # Spuštění jednou denně

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'akcie.clean_old_backups_cron_job'

    def do(self):
        backup_dir = 'backups'
        now = time.time()
        retention_period = 7 * 24 * 60 * 60  # 7 dní

        if os.path.exists(backup_dir):
            for filename in os.listdir(backup_dir):
                file_path = os.path.join(backup_dir, filename)
                if os.stat(file_path).st_mtime < now - retention_period:
                    os.remove(file_path)
                    print(f'Smazána stará záloha: {file_path}')
        else:
            print('Adresář pro zálohy neexistuje.')
