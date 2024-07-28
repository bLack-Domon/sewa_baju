from django import forms
from .models import Katalog,Kategori,User,Pelanggan,Sewa,DetailSewa,Slide,Qris,DetailPembayaran
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm

class PelangganRegistrationForm(UserCreationForm):
    nama = forms.CharField(max_length=100, required=True)
    alamat = forms.CharField(max_length=200, required=True)
    nomor_hp = forms.CharField(max_length=20, required=True)

    class Meta:
        model = Pelanggan
        fields = ['nama', 'alamat', 'nomor_hp', 'username', 'email', 'password1', 'password2']
class KatalogForm(forms.ModelForm):
    class Meta:
        model = Katalog
        fields = ['kode', 'nama', 'gambar', 'harga', 'jumlah', 'kategori']

class KategoriForm(forms.ModelForm):
    class Meta:
        model = Kategori
        fields = ['nama', 'ddc']

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class PelangganForm(forms.ModelForm):
    class Meta:
        model = Pelanggan
        fields = ['nama', 'alamat', 'nomor_hp']

class SewaForm(forms.ModelForm):
    class Meta:
        model = Sewa
        fields = ['pelanggan', 'tanggal_pakai', 'tanggal_ambil', 'tanggal_kembalikan']

class DetailSewaForm(forms.ModelForm):
    class Meta:
        model = DetailSewa
        fields = ['katalog', 'jumlah']

class SlideForm(forms.ModelForm):
    class Meta:
        model = Slide
        fields = ['gambar', 'keterangan']
        widgets = {
            'gambar': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'keterangan': forms.TextInput(attrs={'class': 'form-control'}),
        }
class QrisForm(forms.ModelForm):
    class Meta:
        model = Qris
        fields = ['image']

class DetailPembayaranForm(forms.ModelForm):
    class Meta:
        model = DetailPembayaran
        fields = ['bukti_file_pembayaran']
DetailSewaFormSet = inlineformset_factory(Sewa, DetailSewa, form=DetailSewaForm, extra=1)
