from django.urls import path
from django.contrib.auth import views as auth_views
from django.http import JsonResponse
from django.views import View
from . import views
from .views import user_preferences, export_hot_investments_csv, search_stocks, add_stock, history_dates, auditlog_list
from .views import klient_list, klient_create, klient_update, klient_delete, portfolio_list, portfolio_create, portfolio_update, portfolio_delete
from .views import export_klienti_csv, export_klienti_excel, export_portfolia_csv, export_portfolia_excel, export_klienti_pdf, export_portfolia_pdf

class HealthCheckView(View):
    def get(self, request):
        from django.db import connection
        try:
            connection.ensure_connection()
            return JsonResponse({'status': 'ok', 'db': 'ok'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'db': str(e)}, status=500)

urlpatterns = [
    path('', views.index, name='index'),
    path('akcie/', views.akcie_list, name='akcie_list'),
    path('akcie/<int:pk>/', views.akcie_detail, name='akcie_detail'),
    path('akcie/create/', views.akcie_create, name='akcie_create'),
    path('akcie/<int:pk>/update/', views.akcie_update, name='akcie_update'),
    path('akcie/<int:pk>/delete/', views.akcie_delete, name='akcie_delete'),
    path('akcie/export/', views.export_akcie_csv, name='export_akcie_csv'),
    path('akcie/import/', views.import_akcie_csv, name='import_akcie_csv'),
    path('akcie/report/', views.generate_akcie_pdf, name='generate_akcie_pdf'),
    path('akcie/import_excel/', views.import_excel, name='import_excel'),
    path('akcie/export_excel/', views.export_excel, name='export_excel'),
    path('akcie/export_json/', views.export_akcie_json, name='export_akcie_json'),
    path('akcie/search/', search_stocks, name='search_stocks'),
    path('akcie/add/', add_stock, name='add_stock'),
    path('akcie/history_dates/', history_dates, name='history_dates'),
    path('transakce/', views.transakce_list, name='transakce_list'),
    path('transakce/<int:pk>/', views.transakce_detail, name='transakce_detail'),
    path('transakce/create/', views.transakce_create, name='transakce_create'),
    path('transakce/<int:pk>/update/', views.transakce_update, name='transakce_update'),
    path('transakce/<int:pk>/delete/', views.transakce_delete, name='transakce_delete'),
    path('transakce/export/', views.export_transakce_csv, name='export_transakce_csv'),
    path('transakce/report/', views.generate_transakce_pdf, name='generate_transakce_pdf'),
    path('dividendy/', views.dividenda_list, name='dividenda_list'),
    path('dividendy/<int:pk>/', views.dividenda_detail, name='dividenda_detail'),
    path('dividendy/create/', views.dividenda_create, name='dividenda_create'),
    path('dividendy/<int:pk>/update/', views.dividenda_update, name='dividenda_update'),
    path('dividendy/<int:pk>/delete/', views.dividenda_delete, name='dividenda_delete'),
    path('dividendy/export/', views.export_dividendy_csv, name='export_dividendy_csv'),
    path('dividendy/report/', views.generate_dividenda_pdf, name='generate_dividenda_pdf'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/export/', views.export_dashboard_pdf, name='export_dashboard_pdf'),
    path('dashboard/export_graphs_pdf/', views.export_dashboard_graphs_pdf, name='export_dashboard_graphs_pdf'),
    path('poradce/dashboard/', views.poradce_dashboard, name='poradce_dashboard'),
    path('aktivity/', views.aktivity_list, name='aktivity_list'),
    path('aktivity/export_csv/', views.export_aktivity_csv, name='export_aktivity_csv'),
    path('aktivity/export_pdf/', views.export_aktivity_pdf, name='export_aktivity_pdf'),
    path('login/', auth_views.LoginView.as_view(template_name='akcie/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('preferences/', user_preferences, name='user_preferences'),
    path('export_all_data_zip/', views.export_all_data_zip, name='export_all_data_zip'),
    path('export-hot-investments/', export_hot_investments_csv, name='export_hot_investments_csv'),
    path('convert_to_czk/', views.convert_to_czk_api, name='convert_to_czk_api'),
    path('api/akcie/', views.api_akcie_list, name='api_akcie_list'),
    path('api/transakce/', views.api_transakce_list, name='api_transakce_list'),
    path('api/dividendy/', views.api_dividenda_list, name='api_dividenda_list'),
    path('health/', HealthCheckView.as_view(), name='health'),
    path('auditlog/', auditlog_list, name='auditlog_list'),
    path('klienti/', views.klienti, name='klienti'),
    path('reporty/', views.reporty, name='reporty'),
    path('analyzy/', views.analyzy, name='analyzy'),
    path('upozorneni/', views.upozorneni, name='upozorneni'),
    path('nastaveni/', views.nastaveni, name='nastaveni'),
    path('vip/', views.vip, name='vip'),
    path('chat/', views.chat, name='chat'),
    path('integrace/', views.integrace, name='integrace'),
    path('klienti/', klient_list, name='klient_list'),
    path('klienti/create/', klient_create, name='klient_create'),
    path('klienti/<int:pk>/update/', klient_update, name='klient_update'),
    path('klienti/<int:pk>/delete/', klient_delete, name='klient_delete'),
    path('klienti/<int:klient_id>/portfolia/', portfolio_list, name='portfolio_list'),
    path('klienti/<int:klient_id>/portfolia/create/', portfolio_create, name='portfolio_create'),
    path('klienti/<int:klient_id>/portfolia/<int:pk>/update/', portfolio_update, name='portfolio_update'),
    path('klienti/<int:klient_id>/portfolia/<int:pk>/delete/', portfolio_delete, name='portfolio_delete'),
    path('klienti/export/csv/', export_klienti_csv, name='export_klienti_csv'),
    path('klienti/export/excel/', export_klienti_excel, name='export_klienti_excel'),
    path('klienti/<int:klient_id>/portfolia/export/csv/', export_portfolia_csv, name='export_portfolia_csv'),
    path('klienti/<int:klient_id>/portfolia/export/excel/', export_portfolia_excel, name='export_portfolia_excel'),
    path('klienti/export/pdf/', export_klienti_pdf, name='export_klienti_pdf'),
    path('klienti/<int:klient_id>/portfolia/export/pdf/', export_portfolia_pdf, name='export_portfolia_pdf'),
    path('admin/klienti/', views.klient_list_admin, name='klient_list_admin'),
    path('poradce/klient/<int:klient_id>/report_pdf/', views.klient_report_pdf, name='klient_report_pdf'),
    path('poradce/klient/<int:klient_id>/send_report/', views.klient_report_send_email, name='klient_report_send_email'),
]
