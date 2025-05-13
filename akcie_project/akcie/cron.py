from django_cron import CronJobBase, Schedule
from .views import export_dashboard_graphs_pdf, send_monthly_report

class MonthlyReportCronJob(CronJobBase):
    RUN_EVERY_MINS = 0  # Spouští se jednou za měsíc

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'akcie.monthly_report_cron_job'

    def do(self):
        send_monthly_report()
