from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('akcie/', views.akcie_list, name='akcie_list'),
    path('akcie/<int:pk>/', views.akcie_detail, name='akcie_detail'),
    path('akcie/create/', views.akcie_create, name='akcie_create'),
    path('akcie/<int:pk>/update/', views.akcie_update, name='akcie_update'),
    path('akcie/<int:pk>/delete/', views.akcie_delete, name='akcie_delete'),
    path('transakce/', views.transakce_list, name='transakce_list'),
    path('transakce/<int:pk>/', views.transakce_detail, name='transakce_detail'),
    path('transakce/create/', views.transakce_create, name='transakce_create'),
    path('transakce/<int:pk>/update/', views.transakce_update, name='transakce_update'),
    path('transakce/<int:pk>/delete/', views.transakce_delete, name='transakce_delete'),
    path('dividendy/', views.dividenda_list, name='dividenda_list'),
    path('dividendy/<int:pk>/', views.dividenda_detail, name='dividenda_detail'),
    path('dividendy/create/', views.dividenda_create, name='dividenda_create'),
    path('dividendy/<int:pk>/update/', views.dividenda_update, name='dividenda_update'),
    path('dividendy/<int:pk>/delete/', views.dividenda_delete, name='dividenda_delete'),
]
