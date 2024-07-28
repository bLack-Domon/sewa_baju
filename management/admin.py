from django.contrib import admin
from .models import Pelanggan, Kategori, Katalog, Sewa, DetailSewa,Slide,Qris,DetailPembayaran

admin.site.register(Pelanggan)
admin.site.register(Kategori)
admin.site.register(Katalog)
admin.site.register(Sewa)
admin.site.register(DetailSewa)
admin.site.register(Slide)
admin.site.register(Qris)
admin.site.register(DetailPembayaran)