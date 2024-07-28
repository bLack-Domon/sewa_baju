"""sewa_baju URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.conf import settings
# from django.conf.urls.static import static
# from django.contrib import admin
# from django.urls import path,include

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

from django.urls import path,include
from management import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.login_view, name='login'),
    path('home/', views.home, name='home'),
    path('pelanggan/', views.pelanggan, name='pelanggan'),
    path('pelanggan/create/', views.pelanggan_create, name='pelanggan_create'),
    path('pelanggan/update/<int:pk>/', views.pelanggan_update, name='pelanggan_update'),
    path('pelanggan/delete/<int:pk>/', views.pelanggan_delete, name='pelanggan_delete'),
    path('kategori/', views.kategori, name='kategori'),
    path('kategori/create/', views.kategori_create, name='kategori_create'),
    path('kategori/update/<int:pk>/', views.kategori_update, name='kategori_update'),
    path('kategori/delete/<int:pk>/', views.kategori_delete, name='kategori_delete'),
    path('katalog/', views.katalog, name='katalog'),
    path('katalog/create/', views.katalog_create, name='katalog_create'),
    path('katalog/update/<int:pk>/', views.katalog_update, name='katalog_update'),
    path('katalog/delete/<int:pk>/', views.katalog_delete, name='katalog_delete'),
    path('sewa/', views.sewa_list, name='sewa'),
    path('laporansewa/', views.laporansewa_list, name='laporansewa'),
    path('export-sewa-excel/', views.export_sewa_excel, name='export_sewa_excel'),
    path('update_status_bayar/<int:sewa_id>/', views.update_status_bayar, name='update_status_bayar'),
    path('tambah-sewa/', views.tambah_sewa, name='tambah_sewa'),
    path('daftar-sewa/', views.daftar_sewa, name='daftar_sewa'),
    path('users/', views.user_list, name='users'),
    path('users/create/', views.user_create, name='user_create'),
    path('users/<int:pk>/update/', views.user_update, name='user_update'),
    path('users/<int:pk>/delete/', views.user_delete, name='user_delete'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),  
    path('slides/', views.slide_list, name='slide_list'),
    path('slides/create/', views.slide_create, name='slide_create'),
    path('slides/update/<int:pk>/', views.slide_update, name='slide_update'),
    path('slides/delete/<int:pk>/', views.slide_delete, name='slide_delete'),

    path('qris/', views.qris_list, name='qris_list'),
    path('qris/create/', views.qris_create, name='qris_create'),
    path('qris/<int:id>/update/', views.qris_update, name='qris_update'),
    path('qris/<int:id>/delete/', views.qris_delete, name='qris_delete'),
    path('update_status_pengembalian/<int:sewa_id>/', views.update_status_pengembalian, name='update_status_pengembalian'),
    path('', include('management.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
