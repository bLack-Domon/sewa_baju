from django.db import models
from django.contrib.auth.models import User

from django.contrib.auth.models import AbstractUser

class Pelanggan(AbstractUser):
    nama = models.CharField(max_length=100, blank=True, null=True)
    alamat = models.CharField(max_length=200, blank=True, null=True)
    nomor_hp = models.CharField(max_length=20, blank=True, null=True)
    

    def __str__(self):
        return self.username

class Kategori(models.Model):
    nama = models.CharField(max_length=100)
    ddc = models.DecimalField(max_digits=10, decimal_places=2)
    def __str__(self):
        return self.nama


class Katalog(models.Model):
    kode = models.CharField(max_length=20)
    nama = models.CharField(max_length=100)
    gambar = models.ImageField(upload_to='media/gambar_katalog/')
    harga = models.PositiveIntegerField(blank=True, null=True)
    jumlah = models.IntegerField()
    kategori = models.ForeignKey(Kategori, on_delete=models.CASCADE)

class Sewa(models.Model):
    BELUM = 'Belum'
    SELESAI = 'Selesai'
    BELUM_SELESAI = 'Belum Selesai'
    PENDING = 'Pending'
    LUNAS = 'Lunas'
    DITOLAK = 'Ditolak'
    TIDAK = 'Tidak'
    BATAL = 'Batal'
    DI_ANTAR = 'Diantar'
    DI_AMBIL = 'Diambil'
    STATUS_CHOICES = [
        (BELUM, 'Belum'),
        (SELESAI, 'Selesai'),
        (BELUM_SELESAI, 'Belum Selesai'),
        (PENDING, 'Pending'),
        (LUNAS, 'Lunas'),
        (DITOLAK, 'Ditolak'),
    ]
    STATUS_CHOICESP = [
        (BELUM, 'Belum'),
        (SELESAI, 'Selesai')
      
    ]
    BATAL_CHOICES = [
        (TIDAK, 'Tidak'),
        (BATAL, 'Batal')
    ]
    TRANSFER = 'Transfer'
    BAYAR_DI_TEMPAT = 'Bayar di Tempat'
    JENIS_PEMBAYARAN_CHOICES = [
        (TRANSFER, 'Transfer'),
        (BAYAR_DI_TEMPAT, 'Bayar di Tempat'),
    ]
    METODE_PENGAMBILAN_CHOICES = [
        (DI_ANTAR, 'Diantar'),
        (DI_AMBIL, 'Diambil'),
    ]
    METODE_PENGEMBALIAN_CHOICES = [
        (DI_ANTAR, 'Diantar'),
        (DI_AMBIL, 'Diambil'),
    ]
    pelanggan = models.ForeignKey(Pelanggan, on_delete=models.CASCADE)
    tanggal_pakai = models.DateField()
    tanggal_ambil = models.DateField()
    tanggal_kembalikan = models.DateField()
    total_harga = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status_bayar = models.CharField(max_length=20, choices=STATUS_CHOICES, default=BELUM)
    status_pengembalian = models.CharField(max_length=20, choices=STATUS_CHOICESP, default=BELUM)
    jenis_pembayaran = models.CharField(max_length=20, choices=JENIS_PEMBAYARAN_CHOICES, default=TRANSFER)
    status_batalpesanan = models.CharField(max_length=20, choices=BATAL_CHOICES, default=TIDAK)
    metode_pengambilan = models.CharField(max_length=20, choices=METODE_PENGAMBILAN_CHOICES, default=DI_ANTAR)
    metode_pengembalian = models.CharField(max_length=20, choices=METODE_PENGEMBALIAN_CHOICES, default=DI_ANTAR)
    def total_harga(self):
        total = 0
        detail_sewa_list = self.detailsewa_set.all()
        for detail_sewa in detail_sewa_list:
            total += detail_sewa.jumlah * detail_sewa.katalog.harga * detail_sewa.jangkasewa
        return total

class DetailSewa(models.Model):
    sewa = models.ForeignKey(Sewa, on_delete=models.CASCADE)
    katalog = models.ForeignKey(Katalog, on_delete=models.CASCADE)
    jumlah = models.IntegerField()
    jangkasewa = models.IntegerField(null=True)
    @property
    def sub_total(self):
        return self.katalog.harga * self.jumlah * self.jangkasewa if self.katalog.harga and self.jumlah and self.jangkasewa else 0

class Slide(models.Model):
    gambar = models.ImageField(upload_to='media/slides/')
    keterangan = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.keterangan or "Slide tanpa keterangan"
    
class Qris(models.Model):
    id = models.AutoField(primary_key=True)
    image = models.ImageField(upload_to='media/qris/')

    def __str__(self):
        return f"QRIS {self.id}"

class DetailPembayaran(models.Model):
    sewa = models.ForeignKey(Sewa, on_delete=models.CASCADE)
    bukti_file_pembayaran = models.ImageField(upload_to='media/detail_pembayaran/')

    def __str__(self):
        return f"Detail Pembayaran untuk Sewa ID {self.sewa.id}"

