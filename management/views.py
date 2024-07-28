from django.shortcuts import render,get_object_or_404,redirect
from .models import Slide, Kategori,Katalog,Pelanggan, Katalog,Sewa,DetailSewa,User,Qris
# from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from datetime import timedelta
from datetime import datetime
from datetime import date
from django.conf import settings
import requests 
import json
from django.contrib.auth import authenticate, login
import pandas as pd
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
# import datetime
from .forms import KatalogForm,KategoriForm,UserForm,PelangganForm,SewaForm, DetailSewaFormSet,SlideForm,QrisForm,DetailPembayaran
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required

from django.db.models import Q
from django.http import HttpResponse, JsonResponse

from .forms import PelangganRegistrationForm
# web============================================================================================================================

from django.core.files.storage import FileSystemStorage

def register_pelanggan(request):
    if request.method == 'POST':
        form = PelangganRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('berandapelanggan')  # Ganti dengan URL yang sesuai setelah login
    else:
        form = PelangganRegistrationForm()
    
    return render(request, 'registerpelanggan.html', {'form': form})
def login_pelanggan(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('berandapelanggan')  # Replace with your desired URL after login
    else:
        form = AuthenticationForm()
    return render(request, 'loginpelanggan.html', {'form': form})


def beranda(request):
    slides = Slide.objects.all()
    kategori_list = Kategori.objects.all()
    
    return render(request, 'beranda.html', {'slides': slides, 'kategori_list': kategori_list})

def kategori_view(request, kategori_id):
    kategori = get_object_or_404(Kategori, pk=kategori_id)
    katalog_list = Katalog.objects.filter(kategori=kategori)
    kategori_list = Kategori.objects.all()
    return render(request, 'kategori.html', {'kategori': kategori, 'katalog_list': katalog_list, 'kategori_list': kategori_list})

from django.shortcuts import render

def pencarian_view(request):
    query = request.GET.get('q')
    kategori_list = Kategori.objects.all()
    katalog_list = None
    kategori = None
    
    if query:
        try:
            # Coba mengonversi query menjadi nilai desimal
            ddc_value = float(query)
            kategori = Kategori.objects.filter(ddc=ddc_value).first()
            if kategori:
                katalog_list = Katalog.objects.filter(kategori=kategori)
            else:
                katalog_list = Katalog.objects.none()
        except ValueError:
            # Jika query tidak dapat dikonversi menjadi desimal, hasilkan kosong
            katalog_list = Katalog.objects.none()
    else:
        katalog_list = Katalog.objects.none()

    return render(request, 'pencarian.html', {'query': query, 'kategori': kategori, 'katalog_list': katalog_list, 'kategori_list': kategori_list})

# def tambah_ke_keranjang(request, katalog_id):
#     katalog = get_object_or_404(Katalog, pk=katalog_id)
#     if request.method == 'POST':
#         jumlah_sewa = int(request.POST.get('jumlah', 0))
#         jangkasewa = int(request.POST.get('jangkasewa', 1))  # Default to 1 (daily) if not provided
#         if jumlah_sewa <= 0 or jangkasewa <= 0:
#             return redirect('kategoripelanggan', kategori_id=katalog.kategori.id)  # Redirect back to category page

#         if jumlah_sewa > katalog.jumlah:
#             # Jika jumlah sewa melebihi stok, tampilkan pesan kesalahan
#             # messages.error(request, 'Jumlah yang diminta melebihi stok yang tersedia.')
#             return redirect('kategori', kategori_id=katalog.kategori.id)  # Redirect back to category page

#         # Hitung subtotal
#         subtotal = jumlah_sewa * katalog.harga * jangkasewa

#         # Simpan item ke keranjang
#         keranjang = request.session.get('keranjang', {})
#         keranjang[katalog_id] = {'jumlah': jumlah_sewa, 'jangkasewa': jangkasewa, 'subtotal': subtotal}
#         request.session['keranjang'] = keranjang

#         # Redirect ke halaman keranjang atau halaman lain yang sesuai
#         return redirect('keranjangpelanggan')  # Ubah 'keranjang' sesuai dengan URL halaman keranjang Anda

#     # Jika request.method bukan POST, atau jika ada kesalahan lain, redirect kembali ke kategori
#     return redirect('kategoripelanggan', kategori_id=katalog.kategori.id)

# def tampil_keranjang(request):
#     kategori_list = Kategori.objects.all()
#     keranjang = request.session.get('keranjang', {})
#     total_harga = 0
#     items = []
#     for katalog_id, data in keranjang.items():  # Loop melalui item-session yang berisi dictionary jumlah dan subtotal
#         katalog = Katalog.objects.get(pk=katalog_id)
#         jumlah_sewa = data['jumlah']
#         subtotal = data['subtotal']
#         total_harga += subtotal
#         items.append({'katalog': katalog, 'jumlah_sewa': jumlah_sewa, 'subtotal': subtotal})
    
#     return render(request, 'keranjang.html', {'items': items, 'total_harga': total_harga,'kategori_list': kategori_list})

# @csrf_exempt
# def update_keranjang(request):
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body)
#             katalog_id = data.get('katalog_id')
#             change = data.get('change')
#             keranjang = request.session.get('keranjang', {})

#             if str(katalog_id) in keranjang:
#                 jumlah_sewa = keranjang[str(katalog_id)]['jumlah'] + change
#                 katalog = Katalog.objects.get(pk=katalog_id)

#                 if jumlah_sewa <= 0:
#                     del keranjang[str(katalog_id)]
#                 elif jumlah_sewa > katalog.jumlah:
#                     return JsonResponse({'status': 'error', 'message': 'Jumlah melebihi stok'}, status=400)
#                 else:
#                     keranjang[str(katalog_id)]['jumlah'] = jumlah_sewa
#                     keranjang[str(katalog_id)]['subtotal'] = jumlah_sewa * katalog.harga

#                 request.session['keranjang'] = keranjang

#                 total_harga = sum(item['subtotal'] for item in keranjang.values())
#                 return JsonResponse({
#                     'status': 'success',
#                     'jumlah_sewa': jumlah_sewa,
#                     'subtotal': keranjang[str(katalog_id)]['subtotal'],
#                     'total_harga': total_harga
#                 })
#         except Exception as e:
#             return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
#     return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)
def tampil_keranjang(request):
    kategori_list = Kategori.objects.all()
    keranjang = request.session.get('keranjang', {})
    total_harga = 0
    items = []
    for katalog_id, data in keranjang.items():
        katalog = Katalog.objects.get(pk=katalog_id)
        jumlah_sewa = int(data['jumlah'])
        jangkasewa = int(data.get('jangkasewa', 1))  # Default to 1 if not provided
        subtotal = int(data['subtotal'])  # Convert to float to avoid type errors
        total_harga += subtotal
        items.append({'katalog': katalog, 'jumlah_sewa': jumlah_sewa, 'jangkasewa': jangkasewa, 'subtotal': subtotal})

    return render(request, 'keranjang.html', {'items': items, 'total_harga': total_harga, 'kategori_list': kategori_list})
def tambah_ke_keranjang(request, katalog_id):
    katalog = get_object_or_404(Katalog, pk=katalog_id)
    if request.method == 'POST':
        jumlah_sewa = int(request.POST.get('jumlah', 0))
        jangkasewa = int(request.POST.get('jangkasewa', 1))  # Default to 1 (daily) if not provided
        if jumlah_sewa <= 0 or jangkasewa <= 0:
            return redirect('kategoripelanggan', kategori_id=katalog.kategori.id)  # Redirect back to category page

        if jumlah_sewa > katalog.jumlah:
            return redirect('kategoripelanggan', kategori_id=katalog.kategori.id)  # Redirect back to category page

        # Hitung subtotal
        subtotal = jumlah_sewa * katalog.harga * jangkasewa

        # Simpan item ke keranjang
        keranjang = request.session.get('keranjang', {})
        keranjang[katalog_id] = {'jumlah': jumlah_sewa, 'jangkasewa': jangkasewa, 'subtotal': float(subtotal)}
        request.session['keranjang'] = keranjang

        # Redirect ke halaman keranjang atau halaman lain yang sesuai
        return redirect('keranjangpelanggan')

    return redirect('kategoripelanggan', kategori_id=katalog.kategori.id)

@csrf_exempt
def update_keranjang(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            katalog_id = data.get('katalog_id')
            change = int(data.get('change', 0))  # Ensure change is an integer
            jangkasewa = int(data.get('jangkasewa', 1))  # Ensure jangkasewa is an integer, default to 1 if not provided

            keranjang = request.session.get('keranjang', {})

            if str(katalog_id) in keranjang:
                jumlah_sewa = int(keranjang[str(katalog_id)]['jumlah'])  # Ensure jumlah_sewa is an integer
                jumlah_sewa += change  # Perform the addition

                katalog = Katalog.objects.get(pk=katalog_id)

                if jumlah_sewa <= 0:
                    del keranjang[str(katalog_id)]
                elif jumlah_sewa > katalog.jumlah:
                    return JsonResponse({'status': 'error', 'message': 'Jumlah melebihi stok'}, status=400)
                else:
                    keranjang[str(katalog_id)]['jumlah'] = jumlah_sewa
                    keranjang[str(katalog_id)]['jangkasewa'] = jangkasewa  # Update jangkasewa
                    keranjang[str(katalog_id)]['subtotal'] = jumlah_sewa * katalog.harga * jangkasewa

                request.session['keranjang'] = keranjang

                total_harga = sum(float(item['subtotal']) for item in keranjang.values())  # Convert subtotals to float
                return JsonResponse({
                    'status': 'success',
                    'jumlah_sewa': jumlah_sewa,
                    'subtotal': keranjang[str(katalog_id)]['subtotal'],
                    'total_harga': total_harga
                })
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

@csrf_exempt
def update_keranjang_all(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            jangkasewa = int(data.get('jangkasewa', 1))  # Ensure jangkasewa is an integer, default to 1 if not provided

            keranjang = request.session.get('keranjang', {})

            for item_id, item in keranjang.items():
                katalog = Katalog.objects.get(pk=item_id)
                item['jangkasewa'] = jangkasewa
                item['subtotal'] = item['jumlah'] * katalog.harga * jangkasewa

            request.session['keranjang'] = keranjang

            total_harga = sum(float(item['subtotal']) for item in keranjang.values())  # Convert subtotals to float
            return JsonResponse({
                'status': 'success',
                'total_harga': total_harga,
                'keranjang': keranjang
            })
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

from datetime import datetime, timedelta
from django.shortcuts import redirect
from .models import Sewa, DetailSewa, Katalog
def simpan_sewa(request):
    if request.method == 'POST':
        # Ambil data dari formulir
        nama = request.user.nama
        alamat = request.user.alamat
        nomor_hp = request.user.nomor_hp
        tanggal_pakai = request.POST['tanggal_pakai']
        tanggal_ambil = request.POST['tanggal_ambil']
        tanggal_kembalikan = request.POST['tanggal_kembalikan']
        metode_pengambilan = request.POST['metode_pengambilan']
        metode_pengembalian = request.POST['metode_pengembalian']
        jenis_pembayaran = 'Transfer'
        
        # Simpan data sewa
        sewa = Sewa.objects.create(
            pelanggan=request.user,
            tanggal_pakai=tanggal_pakai,
            tanggal_ambil=tanggal_ambil,
            tanggal_kembalikan=tanggal_kembalikan,
            metode_pengambilan=metode_pengambilan,
            metode_pengembalian=metode_pengembalian
        )
        
        # Simpan detail sewa dari data keranjang (sesi)
        keranjang = request.session.get('keranjang', {})
        for katalog_id, data in keranjang.items():
            jumlah_sewa = data['jumlah']
            jangkasewa = data['jangkasewa']
            katalog = Katalog.objects.get(pk=katalog_id)
            # Update jumlah katalog
            katalog.jumlah -= jumlah_sewa
            katalog.save()
            # Simpan detail sewa
            DetailSewa.objects.create(sewa=sewa, katalog=katalog, jumlah=jumlah_sewa, jangkasewa=jangkasewa)
        
        # Kosongkan sesi keranjang setelah menyimpan data sewa
        request.session['keranjang'] = {}
        # Panggil fungsi untuk mengirim pesan Telegram
        send_telegram_message(nama, alamat, nomor_hp, tanggal_pakai, tanggal_ambil, tanggal_kembalikan, keranjang, jenis_pembayaran)
        return redirect('keranjangpelanggan')
    else:
        return redirect('keranjangpelanggan')

def send_telegram_message(nama, alamat, nomor_hp, tanggal_pakai, tanggal_ambil, tanggal_kembalikan, keranjang, jenis_pembayaran):
    bot_token = settings.TELEGRAM_BOT_TOKEN     
    chat_id = settings.TELEGRAM_CHAT_ID
    
    # Membuat pesan
    message = f'Pesanan baru!\nNama: {nama}\nAlamat: {alamat}\nNomor HP: {nomor_hp}\nTanggal Ambil: {tanggal_ambil}\nTanggal Pakai: {tanggal_pakai}\nTanggal Kembalikan: {tanggal_kembalikan}\nJenis: {jenis_pembayaran}\n\nDetail Keranjang:\n'
    
    for katalog_id, data in keranjang.items():
        katalog = Katalog.objects.get(pk=katalog_id)
        jumlah_sewa = data['jumlah']
        jangkasewa = data['jangkasewa']
        message += f'\nNama Barang: {katalog.nama}\nHarga: {katalog.harga}\nJumlah: {jumlah_sewa}\nJangka Sewa: {jangkasewa}\n'
    
    # Mengirim pesan ke Telegram
    telegram_api_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"     
    payload = {"chat_id": chat_id, "text": message, "parse_mode": "HTML"}    
    requests.post(telegram_api_url, data=payload)


def history_sewa(request):
    kategori_list = Kategori.objects.all()
    sewa_list = Sewa.objects.filter(pelanggan=request.user).order_by('-tanggal_ambil')
    qris = Qris.objects.first()  # Assuming you only have one QRIS record

    today = timezone.now().date()
    for sewa in sewa_list:
        if sewa.tanggal_kembalikan and sewa.tanggal_kembalikan < today:
            days_late = (today - sewa.tanggal_kembalikan).days
            sewa.denda = days_late * 1000
        else:
            sewa.denda = 0

    return render(request, 'history_sewa.html', {'sewa_list': sewa_list, 'qris': qris, 'kategori_list': kategori_list})
def batal_sewa(request):
    if request.method == 'POST':
        sewa_id = request.POST.get('sewa_id')
        try:
            sewa = Sewa.objects.get(id=sewa_id)
            sewa.status_batalpesanan = 'Batal'
            sewa.save()
            messages.success(request, 'Pesanan berhasil dibatalkan.')
        except Sewa.DoesNotExist:
            messages.error(request, 'Pesanan tidak ditemukan.')

    return redirect('history_sewapelanggan')

def syarat_dan_ketentuan(request):
    kategori_list = Kategori.objects.all()
    return render(request, 'syarat_dan_ketentuan.html', {'kategori_list': kategori_list})

def cara_pemesanan(request):
    kategori_list = Kategori.objects.all()
    return render(request, 'cara_pemesanan.html', {'kategori_list': kategori_list})

from django.contrib import messages
import os
from django.core.files.storage import default_storage
from django.conf import settings

def upload_bukti_pembayaran(request):
    if request.method == 'POST' and request.FILES.get('bukti_pembayaran'):
        bukti_pembayaran = request.FILES['bukti_pembayaran']
        sewa_id = request.POST.get('sewa_id')
        if sewa_id:
            try:
                sewa = Sewa.objects.get(id=sewa_id)
                detail_pembayaran = DetailPembayaran(sewa=sewa, bukti_file_pembayaran=bukti_pembayaran)
                detail_pembayaran.save()
                
                sewa.status_bayar = Sewa.PENDING
                sewa.save()

                # Simpan bukti pembayaran ke media directory
                bukti_pembayaran_path = default_storage.save(bukti_pembayaran.name, bukti_pembayaran)
                full_path = os.path.join(settings.MEDIA_ROOT, bukti_pembayaran_path)
                
                # Logging full path for debugging
                logging.info(f'Bukti pembayaran path: {full_path}')
                print(f'Bukti pembayaran path: {full_path}')

                # Panggil fungsi untuk mengirim pesan Telegram dengan foto
                send_telegram_message_with_photo(sewa.pelanggan.nama, sewa.pelanggan.alamat, sewa.pelanggan.nomor_hp, sewa.tanggal_ambil, sewa.tanggal_pakai, sewa.tanggal_kembalikan, full_path)

                messages.success(request, 'Bukti pembayaran berhasil diupload dan status sewa diperbarui menjadi Pending.')
                return redirect('history_sewapelanggan')
            except Sewa.DoesNotExist:
                messages.error(request, 'Sewa tidak ditemukan.')
                return redirect('history_sewapelanggan')
    messages.error(request, 'Permintaan tidak valid.')
    return redirect('history_sewapelanggan')


import logging

def send_telegram_message_with_photo(nama, alamat, nomor_hp, tanggal_ambil, tanggal_pakai, tanggal_kembalikan, bukti_pembayaran_path):
    bot_token = settings.TELEGRAM_BOT_TOKEN     
    chat_id = settings.TELEGRAM_CHAT_ID
    
    # Membuat pesan
    message = f'Bukti Pembayaran Diterima!\nNama: {nama}\nAlamat: {alamat}\nNomor HP: {nomor_hp}\nTanggal Ambil: {tanggal_ambil}\nTanggal Pakai: {tanggal_pakai}\nTanggal Kembalikan: {tanggal_kembalikan}\n\nLihat bukti pembayaran terlampir.'
    
    # Mengirim pesan ke Telegram dengan foto
    telegram_api_url = f"https://api.telegram.org/bot{bot_token}/sendPhoto"
    with open(bukti_pembayaran_path, 'rb') as photo_file:
        response = requests.post(telegram_api_url, data={
            "chat_id": chat_id,
            "caption": message,
            "parse_mode": "HTML"
        }, files={"photo": photo_file})

    # Log the response for debugging
    logging.info(f'Telegram response: {response.text}')
    print(f'Telegram response: {response.text}')




def get_detail_pembayaran(request, sewa_id):
    try:
        detail_pembayaran = DetailPembayaran.objects.filter(sewa_id=sewa_id).order_by('-id').first()
        if detail_pembayaran:
            image_url = detail_pembayaran.bukti_file_pembayaran.url
            return JsonResponse({'success': True, 'image_url': image_url})
        else:
            return JsonResponse({'success': False, 'error': 'Detail Pembayaran tidak ditemukan'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

# def send_telegram_message(nama, alamat, nomor_hp, tanggal_ambil, tanggal_pakai, tanggal_kembalikan, keranjang,jenis_pembayaran):
#     bot_token = settings.TELEGRAM_BOT_TOKEN     
#     chat_id = settings.TELEGRAM_CHAT_ID
    
#     # Membuat pesan
#     message = f'Pesanan baru!\nNama: {nama}\nAlamat: {alamat}\nNomor HP: {nomor_hp}\nTanggal Ambil: {tanggal_ambil}\nTanggal Pakai: {tanggal_pakai}\nTanggal Kembalikan: {tanggal_kembalikan}\nJenis: {jenis_pembayaran}\n\nDetail Keranjang:\n'
    
#     for katalog_id, jumlah_sewa,jangkasewa in keranjang.items():
#         katalog = Katalog.objects.get(pk=katalog_id)
#         message += f'\nNama Barang: {katalog.nama}\nHarga: {katalog.harga}\nJumlah: {jumlah_sewa}\nJangka sewa: {jangkasewa}\n'
    
#     # Mengirim pesan ke Telegram
#     telegram_api_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"     
#     payload = {"chat_id": chat_id, "text": message, "parse_mode": "HTML"}    
#     requests.post(telegram_api_url, data=payload)


 


# ==admin==============================================================================================================

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect ke halaman setelah login berhasil
            return redirect('home')
        else:
            # Tampilkan pesan error jika login gagal
            error_message = "Invalid username or password."
            return render(request, 'admin/adminlogin.html', {'error_message': error_message})
    else:
        return render(request, 'admin/adminlogin.html')
from django.contrib.auth.decorators import user_passes_test

def is_superadmin(user):
    return user.is_superuser   
@login_required
@user_passes_test(is_superadmin)
def home(request):
    pelanggan_count = Pelanggan.objects.exclude(is_superuser=True).count()
    kategori_count = Kategori.objects.count()
    katalog_count = Katalog.objects.count()
    sewa_count = Sewa.objects.count()

    pelanggan = Pelanggan.objects.all()
    kategori = Kategori.objects.all()
    katalog = Katalog.objects.all()
    sewa = Sewa.objects.all()

    return render(request, 'admin/home.html', {'pelanggan': pelanggan, 'pelanggan_count': pelanggan_count,
                                         'kategori': kategori, 'kategori_count': kategori_count,
                                         'katalog': katalog, 'katalog_count': katalog_count,'sewa': sewa, 'sewa_count': sewa_count})



@login_required
@user_passes_test(is_superadmin)
def pelanggan(request):
    # Ambil semua pengguna yang bukan superadmin
    pelanggan_list = Pelanggan.objects.exclude(is_superuser=True)

    # Penanganan pencarian
    q = request.GET.get('q')
    if q:
        pelanggan_list = pelanggan_list.filter(nama__icontains=q)

    # Pagination
    paginator = Paginator(pelanggan_list, 10)  # Menampilkan 10 item per halaman
    page = request.GET.get('page')
    try:
        pelanggan_list = paginator.page(page)
    except PageNotAnInteger:
        pelanggan_list = paginator.page(1)
    except EmptyPage:
        pelanggan_list = paginator.page(paginator.num_pages)

    return render(request, 'admin/pelanggan.html', {'pelanggan_list': pelanggan_list})


def pelanggan_create(request):
    if request.method == 'POST':
        form = PelangganForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('pelanggan')
    else:
        form = PelangganForm()
    return render(request, 'admin/pelanggan_create.html', {'form': form})

def pelanggan_update(request, pk):
    pelanggan = get_object_or_404(Pelanggan, pk=pk)
    if request.method == 'POST':
        form = PelangganForm(request.POST, instance=pelanggan)
        if form.is_valid():
            form.save()
            return redirect('pelanggan')
    else:
        form = PelangganForm(instance=pelanggan)
    return render(request, 'admin/pelanggan_update.html', {'form': form, 'pelanggan': pelanggan})

def pelanggan_delete(request, pk):
    pelanggan = get_object_or_404(Pelanggan, pk=pk)
    if request.method == 'POST':
        pelanggan.delete()
        return redirect('pelanggan')
    return render(request, 'admin/pelanggan_confirm_delete.html', {'pelanggan': pelanggan})

@login_required
@user_passes_test(is_superadmin)
def kategori(request):
    kategori_list = Kategori.objects.all()

    # Penanganan pencarian
    q = request.GET.get('q')
    if q:
        kategori_list = kategori_list.filter(nama__icontains=q)

    # Pagination
    paginator = Paginator(kategori_list, 10) # Menampilkan 10 item per halaman
    page = request.GET.get('page')
    try:
        kategori_list = paginator.page(page)
    except PageNotAnInteger:
        kategori_list = paginator.page(1)
    except EmptyPage:
        kategori_list = paginator.page(paginator.num_pages)

    return render(request, 'admin/kategori_admin.html', {'kategori_list': kategori_list})
def kategori_create(request):
    if request.method == 'POST':
        form = KategoriForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('kategori')
    else:
        form = KategoriForm()
    return render(request, 'admin/kategori_create.html', {'form': form})

def kategori_update(request, pk):
    kategori = get_object_or_404(Kategori, pk=pk)
    if request.method == 'POST':
        form = KategoriForm(request.POST, instance=kategori)
        if form.is_valid():
            form.save()
            return redirect('kategori')
    else:
        form = KategoriForm(instance=kategori)
    return render(request, 'admin/kategori_update.html', {'form': form})

def kategori_delete(request, pk):
    kategori = get_object_or_404(Kategori, pk=pk)
    if request.method == 'POST':
        kategori.delete()
        return redirect('kategori')
    return render(request, 'admin/kategori_confirm_delete.html', {'kategori': kategori})

@login_required
@user_passes_test(is_superadmin)
def katalog(request):
    katalog_list = Katalog.objects.all()

    # Penanganan pencarian
    q = request.GET.get('q')
    if q:
        katalog_list = katalog_list.filter(nama__icontains=q)

    # Pagination
    paginator = Paginator(katalog_list, 10) # Menampilkan 10 item per halaman
    page = request.GET.get('page')
    try:
        katalog_list = paginator.page(page)
    except PageNotAnInteger:
        katalog_list = paginator.page(1)
    except EmptyPage:
        katalog_list = paginator.page(paginator.num_pages)

    return render(request, 'admin/katalog_admin.html', {'katalog_list': katalog_list})



def katalog_create(request):
    if request.method == 'POST':
        form = KatalogForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('katalog')
    else:
        form = KatalogForm()
    
    # Ambil semua kategori
    kategori_list = Kategori.objects.all()
    
    return render(request, 'admin/katalog_create.html', {'form': form, 'kategori_list': kategori_list})


def katalog_update(request, pk):
    katalog = get_object_or_404(Katalog, pk=pk)
    kategori_list = Kategori.objects.all()  # Ambil semua objek kategori
    if request.method == 'POST':
        form = KatalogForm(request.POST, request.FILES, instance=katalog)
        if form.is_valid():
            form.save()
            return redirect('katalog')
    else:
        form = KatalogForm(instance=katalog)
    return render(request, 'admin/katalog_update.html', {'form': form, 'kategori_list': kategori_list})

def katalog_delete(request, pk):
    katalog = get_object_or_404(Katalog, pk=pk)
    if request.method == 'POST':
        katalog.delete()
        return redirect('katalog')
    return render(request, 'admin/katalog_confirm_delete.html', {'katalog': katalog})



from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import date, datetime
from .models import Sewa

def sewa_list(request):
    today = date.today()
    sewa_list = Sewa.objects.all()

    # Pencarian berdasarkan nama pelanggan
    query = request.GET.get("q", "")
    if query:
        sewa_list = sewa_list.filter(pelanggan__nama__icontains=query)

    # Pencarian berdasarkan rentang tanggal
    start_date_str = request.GET.get("start_date")
    end_date_str = request.GET.get("end_date")

    if start_date_str and end_date_str:
        try:
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
            sewa_list = sewa_list.filter(tanggal_pakai__range=[start_date, end_date])
        except ValueError:
            # Tangkap kesalahan jika format tanggal tidak sesuai
            pass

    # Menghitung denda
    for sewa in sewa_list:
        if sewa.tanggal_kembalikan and sewa.tanggal_kembalikan < today:
            days_late = (today - sewa.tanggal_kembalikan).days
            sewa.denda = days_late * 1000
        else:
            sewa.denda = 0

    paginator = Paginator(sewa_list, 10)
    page = request.GET.get('page')

    try:
        sewa_list = paginator.page(page)
    except PageNotAnInteger:
        sewa_list = paginator.page(1)
    except EmptyPage:
        sewa_list = paginator.page(paginator.num_pages)

    return render(request, 'admin/sewa.html', {
        'sewa_list': sewa_list,
        'today': today,
        'query': query,
        'start_date': start_date_str,
        'end_date': end_date_str,
    })
def laporansewa_list(request):
    today = date.today()
    sewa_list = Sewa.objects.all()

    # Pencarian berdasarkan nama pelanggan
    query = request.GET.get("q", "")
    if query:
        sewa_list = sewa_list.filter(pelanggan__nama__icontains=query)

    # Pencarian berdasarkan rentang tanggal
    start_date_str = request.GET.get("start_date")
    end_date_str = request.GET.get("end_date")

    if start_date_str and end_date_str:
        try:
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
            sewa_list = sewa_list.filter(tanggal_pakai__range=[start_date, end_date])
        except ValueError:
            # Tangkap kesalahan jika format tanggal tidak sesuai
            pass

    paginator = Paginator(sewa_list, 10)
    page = request.GET.get('page')

    try:
        sewa_list = paginator.page(page)
    except PageNotAnInteger:
        sewa_list = paginator.page(1)
    except EmptyPage:
        sewa_list = paginator.page(paginator.num_pages)

    return render(request, 'admin/laporansewa.html', {
        'sewa_list': sewa_list,
        'today': today,
        'query': query,
        'start_date': start_date_str,
        'end_date': end_date_str,
    })
def export_sewa_excel(request):
    query = request.GET.get('q', '')
    start_date_str = request.GET.get('start_date', '')
    end_date_str = request.GET.get('end_date', '')

    # Convert start_date_str and end_date_str to datetime objects or None
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d') if start_date_str != 'None' and start_date_str else None
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d') if end_date_str != 'None' and end_date_str else None

    # Lakukan filtering data berdasarkan query dan rentang tanggal
    sewa_list = Sewa.objects.all()
    if query:
        sewa_list = sewa_list.filter(pelanggan__nama__icontains=query)
    if start_date and end_date:
        sewa_list = sewa_list.filter(tanggal_pesan__range=[start_date, end_date])

    # Buat DataFrame dari data Sewa
    data = {
        'No.': [index + 1 for index, sewa in enumerate(sewa_list)],
        'Pelanggan': [sewa.pelanggan.nama for sewa in sewa_list],
        'Tgl Pakai': [sewa.tanggal_pakai for sewa in sewa_list],
        'Tgl Ambil': [sewa.tanggal_ambil for sewa in sewa_list],
        'Tgl Kembali': [sewa.tanggal_kembalikan for sewa in sewa_list],
        'Total Harga': [sewa.total_harga() if hasattr(sewa, 'total_harga') else '' for sewa in sewa_list],
        'Jenis Pembayaran': [sewa.jenis_pembayaran for sewa in sewa_list],
        'Status Bayar': ['Belum' if sewa.status_bayar == 'Belum' else 'Selesai' for sewa in sewa_list],
        'Status Pengembalian': [sewa.status_pengembalian for sewa in sewa_list],
    }
    df = pd.DataFrame(data)

    # Buat response dengan tipe konten Excel
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="data_sewa.xlsx"'

    # Tulis DataFrame ke file Excel
    df.to_excel(response, index=False)

    return response

# def export_sewa_excel(request):
#     query = request.GET.get('q', '')
#     start_date_str = request.GET.get('start_date', '')
#     end_date_str = request.GET.get('end_date', '')

#     # Convert start_date_str and end_date_str to datetime objects or None
#     start_date = datetime.strptime(start_date_str, '%Y-%m-%d') if start_date_str != 'None' and start_date_str else None
#     end_date = datetime.strptime(end_date_str, '%Y-%m-%d') if end_date_str != 'None' and end_date_str else None

#     # Lakukan filtering data berdasarkan query dan rentang tanggal
#     sewa_list = Sewa.objects.all()
#     if query:
#         sewa_list = sewa_list.filter(pelanggan__nama__icontains=query)
#     if start_date and end_date:
#         sewa_list = sewa_list.filter(tanggal_pesan__range=[start_date, end_date])

#     # Buat DataFrame dari data Sewa
#     data = {
#         'No.': [index + 1 for index, sewa in enumerate(sewa_list)],
#         'Nama Pelanggan': [sewa.pelanggan.nama for sewa in sewa_list],
#         'Tanggal Pesan': [sewa.tanggal_pesan for sewa in sewa_list],
#         'Jangka Sewa': [sewa.jangka_sewa for sewa in sewa_list],
#         'Jatuh Tempo': [sewa.tanggal_jatuh_tempo for sewa in sewa_list],
#         'Total Harga': [sewa.total_harga() if hasattr(sewa, 'total_harga') else '' for sewa in sewa_list],
#         'Bayar': ['Belum' if sewa.status_bayar == 'Belum' else 'Selesai' for sewa in sewa_list],
#         'Pengembalian': ['' for sewa in sewa_list],
#         'Denda': [sewa.late_fee if hasattr(sewa, 'late_fee') else '' for sewa in sewa_list],
#         'Telat (hari)': [sewa.days_late if hasattr(sewa, 'days_late') else '' for sewa in sewa_list],
#     }
#     df = pd.DataFrame(data)

#     # Buat response dengan tipe konten Excel
#     response = HttpResponse(content_type='application/vnd.ms-excel')
#     response['Content-Disposition'] = 'attachment; filename="data_sewa.xlsx"'

#     # Tulis DataFrame ke file Excel
#     df.to_excel(response, index=False)

#     return response

# 
def update_status_bayar(request, sewa_id):
    if request.method == 'POST':
        sewa = get_object_or_404(Sewa, id=sewa_id)
        status = request.POST.get('status')
        if status in ['Lunas', 'Ditolak']:
            sewa.status_bayar = status
            sewa.save()
            return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'failed'}, status=400)

from django.views.decorators.http import require_POST
@csrf_exempt
@require_POST
def update_status_pengembalian(request, sewa_id):
    status = request.POST.get('status')
    try:
        sewa = Sewa.objects.get(pk=sewa_id)
        sewa.status_pengembalian = status
        sewa.save()
        return JsonResponse({'success': True})
    except Sewa.DoesNotExist:
        return JsonResponse({'error': 'Sewa not found'}, status=404)
    
@login_required
@login_required
def user_list(request):
    users = Pelanggan.objects.all()  # Gunakan Pelanggan bukan User
    return render(request, 'admin/user_list.html', {'users': users})

def user_create(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        user = Pelanggan.objects.create_user(username=username, email=email, password=password)
        return redirect('users')
    return render(request, 'admin/user_create.html', {'form_title': 'Tambah Pengguna'})

def user_update(request, pk):
    user = get_object_or_404(Pelanggan, pk=pk)  # Mengambil pengguna berdasarkan ID
    if request.method == 'POST':
        user.username = request.POST['username']
        user.email = request.POST['email']
        if 'password' in request.POST and request.POST['password']:
            user.set_password(request.POST['password'])
        user.save()
        return redirect('users')  # Redirect ke daftar pengguna setelah berhasil
    return render(request, 'admin/user_update.html', {'form_title': 'Edit Pengguna', 'user': user})

def user_delete(request, pk):
    user = get_object_or_404(Pelanggan, pk=pk)  # Gunakan Pelanggan bukan User
    if request.method == 'POST':
        user.delete()
        return redirect('users')
    return render(request, 'admin/user_confirm_delete.html', {'user': user})
# web
def tambah_sewa(request):
    if request.method == 'POST':
        sewa_form = SewaForm(request.POST)
        detail_sewa_formset = DetailSewaFormSet(request.POST)
        if sewa_form.is_valid() and detail_sewa_formset.is_valid():
            sewa = sewa_form.save()
            detail_sewa_formset.instance = sewa
            detail_sewa_formset.save()
            return redirect('daftar_sewa')  # Ganti dengan URL yang sesuai
    else:
        sewa_form = SewaForm()
        detail_sewa_formset = DetailSewaFormSet()
    return render(request, 'admin/tambah_sewa.html', {'sewa_form': sewa_form, 'detail_sewa_formset': detail_sewa_formset})

def daftar_sewa(request):
    # Logika untuk menampilkan daftar sewa
    return render(request, 'admin/daftar_sewa.html')

def slide_list(request):
    slides = Slide.objects.all()
    return render(request, 'admin/slide_list.html', {'slides': slides})

def slide_create(request):
    if request.method == 'POST':
        form = SlideForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('slide_list')
    else:
        form = SlideForm()
    return render(request, 'admin/slide_create.html', {'form': form, 'form_title': 'Tambah Slide'})

def slide_update(request, pk):
    slide = get_object_or_404(Slide, pk=pk)
    if request.method == 'POST':
        form = SlideForm(request.POST, request.FILES, instance=slide)
        if form.is_valid():
            form.save()
            return redirect('slide_list')
    else:
        form = SlideForm(instance=slide)
    return render(request, 'admin/slide_update.html', {'form': form, 'form_title': 'Edit Slide'})

def slide_delete(request, pk):
    slide = get_object_or_404(Slide, pk=pk)
    if request.method == 'POST':
        slide.delete()
        return redirect('slide_list')
    return render(request, 'admin/slide_confirm_delete.html', {'slide': slide})

def qris_list(request):
    qris = Qris.objects.all()
    return render(request, 'admin/qris_list.html', {'qris': qris})

def qris_create(request):
    if request.method == 'POST':
        form = QrisForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('qris_list')
    else:
        form = QrisForm()
    return render(request, 'admin/qris_form.html', {'form': form})

def qris_update(request, id):
    qris = get_object_or_404(Qris, id=id)
    if request.method == 'POST':
        form = QrisForm(request.POST, request.FILES, instance=qris)
        if form.is_valid():
            form.save()
            return redirect('qris_list')
    else:
        form = QrisForm(instance=qris)
    return render(request, 'admin/qris_form.html', {'form': form})

def qris_delete(request, id):
    qris = get_object_or_404(Qris, id=id)
    if request.method == 'POST':
        qris.delete()
        return redirect('qris_list')
    return render(request, 'admin/qris_confirm_delete.html', {'qris': qris})












