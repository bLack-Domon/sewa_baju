from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', views.beranda, name='berandapelanggan'),
    path('kategoripelanggan/<int:kategori_id>/', views.kategori_view, name='kategoripelanggan'),
    path('tambah-ke-keranjang/<int:katalog_id>/', views.tambah_ke_keranjang, name='tambah_ke_keranjangpelanggan'),
    path('keranjang/', views.tampil_keranjang, name='keranjangpelanggan'),
    path('update-keranjang/', views.update_keranjang, name='update_keranjangpelanggan'),  # Path untuk update keranjang
    path('update_keranjang_all/', views.update_keranjang_all, name='update_keranjang_all'),

    path('simpan-sewa/', views.simpan_sewa, name='simpan_sewapelanggan'),
    path('pencarianpelanggan/', views.pencarian_view, name='pencarianpelanggan'),
    path('syarat-dan-ketentuan/', views.syarat_dan_ketentuan, name='syarat_dan_ketentuan'),
    path('cara-pemesanan/', views.cara_pemesanan, name='cara_pemesanan'),

    path('registerpelanggan/', views.register_pelanggan, name='registerpelanggan'),
    path('loginpelanggan/', views.login_pelanggan, name='loginpelanggan'),
    # path('history-sewapelanggan/', views.history_sewa, name='history_sewapelanggan'),
    path('history-sewapelanggan/', views.history_sewa, name='history_sewapelanggan'),
    path('generate_midtrans_token/', views.generate_midtrans_token, name='generate_midtrans_token'),
    path('batal-sewa/', views.batal_sewa, name='batal_sewa'),
    path('upload_bukti_pembayaran/', views.upload_bukti_pembayaran, name='upload_bukti_pembayaran'),
    path('get_detail_pembayaran/<int:sewa_id>/', views.get_detail_pembayaran, name='get_detail_pembayaran'),
    path('logoutpelanggan/', views.logout_pelanggan, name='logoutpelanggan'),
    # admin

    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)