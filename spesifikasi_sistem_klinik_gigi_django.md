# Spesifikasi Sistem Klinik Gigi Berbasis Django

## 1. Tujuan Sistem

Sistem Klinik Gigi digunakan untuk mengelola alur pelayanan pasien
secara sederhana mulai dari:

**Pendaftaran → Check-in → Antrean → Panggil → Pemeriksaan Dokter → CPPT
→ Resep → Selesai**

Aplikasi dikembangkan menggunakan **Python + Django** dan dirancang agar
mudah digunakan melalui komputer maupun perangkat mobile.

------------------------------------------------------------------------

## 2. Teknologi

-   Backend: **Python + Django**
-   Database: **MySQL / MariaDB**
-   Frontend: **Django Template + Bootstrap**
-   Interaksi dinamis: **HTMX**
-   Authentication: **Django Authentication**
-   QR Code: untuk **Daftar Mandiri** dan **Check-in**
-   Deployment: **Docker + Gunicorn + Nginx**

## 2.1 Nama Database :
-   database : nentis
-   user : sik
-   pass : 00
-   host : localhost

------------------------------------------------------------------------

## 3. Aktor Sistem

### 3.1 Pasien

Pasien dapat:

-   Mendaftar secara mandiri melalui QR Code.
-   Melakukan pendaftaran sebelum datang ke klinik.
-   Melakukan check-in ketika sudah berada di klinik.
-   Scan QR Code khusus check-in.
-   Mendapat nomor antrean setelah check-in berhasil.
-   Menunggu panggilan pelayanan.

### 3.2 Petugas Admisi

Petugas dapat:

-   Mendaftarkan pasien yang datang langsung.
-   Mencari pasien lama.
-   Membuat kunjungan pasien.
-   Melakukan check-in pasien.
-   Melihat antrean hari ini.
-   Menekan tombol **Panggil**.
-   Melihat status pelayanan.

### 3.3 Dokter Gigi

Dokter dapat:

-   Melihat daftar pasien yang menunggu.
-   Membuka pemeriksaan pasien.
-   Melihat identitas pasien.
-   Melihat riwayat kunjungan.
-   Melihat CPPT sebelumnya.
-   Mengisi CPPT/SOAP.
-   Membuat resep obat.
-   Menyelesaikan pelayanan.

### 3.4 Administrator

Administrator dapat:

-   Mengelola user.
-   Mengelola dokter.
-   Mengelola petugas.
-   Mengelola master obat.
-   Mengatur konfigurasi klinik.
-   Melihat data pelayanan.

------------------------------------------------------------------------

# 4. Konsep Pendaftaran dan Antrean

Pendaftaran dan antrean merupakan dua proses yang berbeda.

**Pendaftaran online TIDAK langsung menghasilkan nomor antrean.**

Nomor antrean hanya diberikan ketika pasien sudah berada di klinik dan
melakukan **check-in**.

Contoh:

``` text
07:00 - Andi daftar online
        Belum mendapat nomor antrean

07:30 - Budi datang langsung
        Check-in → Antrean 001

07:35 - Siti datang langsung
        Check-in → Antrean 002

07:40 - Andi tiba di klinik
        Check-in → Antrean 003
```

Walaupun Andi mendaftar paling awal, Andi mendapatkan nomor 003 karena
baru melakukan check-in setelah Budi dan Siti.

Dengan demikian:

**Urutan antrean = urutan waktu CHECK-IN, bukan urutan waktu
PENDAFTARAN.**

------------------------------------------------------------------------

# 5. QR Code

Sistem menyediakan dua QR Code yang berbeda.

## 5.1 QR Daftar Mandiri

Label:

**DAFTAR PASIEN**

QR Code mengarah ke:

``` text
/daftar/
```

Digunakan untuk:

-   Pasien baru.
-   Pasien lama.
-   Pendaftaran sebelum datang.
-   Pendaftaran mandiri di lokasi klinik.

Setelah berhasil:

``` text
Status = TERDAFTAR
Nomor antrean = BELUM ADA
```

Sistem memberikan informasi bahwa pasien harus melakukan check-in ketika
sudah berada di klinik.

------------------------------------------------------------------------

## 5.2 QR Check-in

Label:

**CHECK-IN PASIEN**

QR Code mengarah ke:

``` text
/checkin/
```

QR ini ditempatkan di lokasi klinik.

Pasien yang sudah melakukan pendaftaran online melakukan scan QR ketika
sudah tiba.

Setelah check-in berhasil:

``` text
Status = MENUNGGU
Nomor antrean = dibuat otomatis
Waktu check-in = waktu saat check-in
```

------------------------------------------------------------------------

# 6. Form Pendaftaran Pasien

Data utama pasien:

  Field          Tipe       Keterangan
  -------------- ---------- ---------------------
  Nama Lengkap   Text       Nama lengkap pasien
  Alamat         Textarea   Alamat pasien
  No. HP         Text       Nomor HP/WhatsApp
  No. KTP        Text       NIK/KTP pasien

Validasi:

-   Nama wajib diisi.
-   Nomor HP wajib diisi.
-   NIK dapat digunakan untuk mendeteksi pasien lama.
-   Sistem harus mencegah duplikasi pasien jika memungkinkan.

------------------------------------------------------------------------

# 7. Pendaftaran Online

Alur:

``` text
SCAN QR DAFTAR
      ↓
FORM PENDAFTARAN
      ↓
CARI PASIEN LAMA
      ↓
PASIEN BARU / PASIEN LAMA
      ↓
BUAT PENDAFTARAN
      ↓
STATUS: TERDAFTAR
      ↓
BELUM MENDAPAT NOMOR ANTREAN
```

Setelah pendaftaran, pasien dapat diberikan kode/ID pendaftaran untuk
digunakan saat check-in.

------------------------------------------------------------------------

# 8. Pendaftaran Melalui Admisi

Jika pasien datang tanpa melakukan pendaftaran online:

``` text
PASIEN DATANG
      ↓
PETUGAS CARI PASIEN
      ↓
PASIEN LAMA?
   ↙       ↘
 YA       TIDAK
 ↓          ↓
PILIH     DAFTARKAN
PASIEN    PASIEN BARU
   ↘       ↙
    BUAT KUNJUNGAN
          ↓
       CHECK-IN
          ↓
    NOMOR ANTREAN
```

Petugas dapat langsung melakukan check-in karena pasien sudah berada
onsite.

------------------------------------------------------------------------

# 9. Proses Check-in

Check-in dapat dilakukan dengan dua cara:

### Check-in Mandiri

Pasien scan **QR CHECK-IN**.

### Check-in oleh Petugas

Petugas mencari pendaftaran pasien lalu menekan:

**CHECK-IN**

Sistem kemudian:

1.  Memastikan pasien memiliki pendaftaran aktif.
2.  Memastikan pasien belum check-in.
3.  Menyimpan waktu check-in.
4.  Mengambil nomor antrean berikutnya.
5.  Membuat data antrean.
6.  Mengubah status menjadi `MENUNGGU`.

------------------------------------------------------------------------

# 10. Nomor Antrean

Nomor antrean dibuat berdasarkan waktu check-in.

Contoh:

``` text
001
002
003
004
005
```

Atau menggunakan prefix:

``` text
A001
A002
A003
```

Nomor dapat di-reset setiap hari.

Contoh:

``` text
Tanggal: 23-07-2026

A001
A002
A003

Tanggal: 24-07-2026

A001
A002
A003
```

Sistem harus mencegah dua pasien mendapatkan nomor antrean yang sama.

------------------------------------------------------------------------

# 11. Status Pelayanan

Status utama:

``` text
TERDAFTAR
    ↓
CHECK-IN
    ↓
MENUNGGU
    ↓
DIPANGGIL
    ↓
DIPERIKSA
    ↓
SELESAI
```

Keterangan:

  Status      Keterangan
  ----------- -------------------------------------------
  TERDAFTAR   Sudah daftar tetapi belum onsite/check-in
  MENUNGGU    Sudah check-in dan mendapat antrean
  DIPANGGIL   Dipanggil oleh petugas
  DIPERIKSA   Sedang diperiksa dokter
  SELESAI     Pelayanan selesai

------------------------------------------------------------------------

# 12. Daftar Antrean Petugas

Contoh:

  No     Nama   Check-in   Status     Aksi
  ------ ------ ---------- ---------- ---------
  A001   Budi   07:30      MENUNGGU   Panggil
  A002   Siti   07:35      MENUNGGU   Panggil
  A003   Andi   07:40      MENUNGGU   Panggil

Petugas menekan:

**PANGGIL**

Status berubah:

``` text
MENUNGGU → DIPANGGIL
```

Daftar antrean disarankan diperbarui menggunakan **HTMX** tanpa reload
halaman penuh.

------------------------------------------------------------------------

# 13. Pemeriksaan Dokter

Dokter memiliki halaman daftar pasien.

Contoh:

  Antrean   Pasien   Status      Aksi
  --------- -------- ----------- ---------
  A001      Budi     DIPANGGIL   Periksa
  A002      Siti     MENUNGGU    \-

Ketika dokter menekan **Periksa**:

``` text
DIPANGGIL → DIPERIKSA
```

Halaman pemeriksaan berisi:

-   Identitas pasien.
-   Riwayat kunjungan.
-   Riwayat CPPT.
-   CPPT saat ini.
-   Resep obat.
-   Tombol selesai.

------------------------------------------------------------------------

# 14. CPPT Pasien

CPPT menggunakan format SOAP.

## Subjective

Keluhan pasien.

## Objective

Hasil pemeriksaan dokter.

## Assessment

Diagnosis/kesimpulan dokter.

## Plan

Rencana atau tindakan.

Struktur:

  Field         Keterangan
  ------------- ------------------
  Tanggal/Jam   Waktu CPPT
  Dokter        Dokter pemeriksa
  Subjective    Keluhan
  Objective     Pemeriksaan
  Assessment    Diagnosis
  Plan          Rencana/tindakan

------------------------------------------------------------------------

# 15. Riwayat Kunjungan

Dokter harus dapat melihat kunjungan pasien sebelumnya.

Contoh:

  Tanggal      Dokter   Assessment   Tindakan
  ------------ -------- ------------ ----------
  01-07-2026   drg. A   Karies 46    Tambal
  10-06-2026   drg. A   Gingivitis   Terapi

Ketika riwayat dibuka, dokter dapat melihat:

-   CPPT lengkap.
-   Diagnosis.
-   Tindakan.
-   Resep sebelumnya.

Riwayat ditampilkan dari yang terbaru.

------------------------------------------------------------------------

# 16. Resep Obat

Dokter dapat membuat resep pada halaman pemeriksaan.

Field resep:

  Field          Keterangan
  -------------- ---------------------
  Nama Obat      Obat yang diberikan
  Jumlah         Jumlah obat
  Dosis          Dosis
  Frekuensi      Frekuensi
  Aturan Pakai   Cara penggunaan
  Keterangan     Informasi tambahan

Satu resep dapat memiliki beberapa obat.

------------------------------------------------------------------------

# 17. Status Selesai

Setelah CPPT dan pelayanan selesai, dokter menekan:

**SELESAI**

Sistem melakukan validasi CPPT.

Status:

``` text
DIPERIKSA → SELESAI
```

Pasien kemudian masuk ke riwayat pelayanan.

------------------------------------------------------------------------

# 18. Struktur Django Project

Struktur aplikasi yang disarankan:

``` text
klinik_gigi/
│
├── config/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── accounts/
│   ├── models.py
│   ├── views.py
│   └── urls.py
│
├── pasien/
│   ├── models.py
│   ├── forms.py
│   ├── views.py
│   └── urls.py
│
├── pendaftaran/
│   ├── models.py
│   ├── forms.py
│   ├── views.py
│   └── urls.py
│
├── antrian/
│   ├── models.py
│   ├── views.py
│   └── urls.py
│
├── pemeriksaan/
│   ├── models.py
│   ├── forms.py
│   ├── views.py
│   └── urls.py
│
├── resep/
│   ├── models.py
│   ├── forms.py
│   ├── views.py
│   └── urls.py
│
├── dashboard/
│   ├── views.py
│   └── urls.py
│
├── templates/
├── static/
├── manage.py
└── requirements.txt
```

------------------------------------------------------------------------

# 19. Model Database Django

## Pasien

``` text
Pasien
- id
- nama_lengkap
- alamat
- no_hp
- no_ktp
- created_at
- updated_at
```

## Pendaftaran

``` text
Pendaftaran
- id
- pasien
- tanggal_kunjungan
- waktu_daftar
- cara_daftar
- kode_pendaftaran
- status
- created_at
```

`cara_daftar`:

``` text
ONLINE
ADMISI
MANDIRI
```

## Antrian

``` text
Antrian
- id
- pendaftaran
- tanggal
- nomor_antrian
- waktu_checkin
- waktu_dipanggil
- status
```

Nomor antrean **tidak disimpan di tabel pendaftaran**, karena nomor baru
dibuat setelah check-in.

## CPPT

``` text
CPPT
- id
- pendaftaran
- dokter
- tanggal_jam
- subjective
- objective
- assessment
- plan
- created_at
- updated_at
```

## Resep

``` text
Resep
- id
- pendaftaran
- dokter
- tanggal
```

## Resep Detail

``` text
ResepDetail
- id
- resep
- nama_obat
- jumlah
- dosis
- frekuensi
- aturan_pakai
- keterangan
```

------------------------------------------------------------------------

# 20. Relasi Database

``` text
PASIEN
  │
  └── PENDAFTARAN
         │
         ├── ANTRIAN
         │
         ├── CPPT
         │
         └── RESEP
                │
                └── RESEP DETAIL
```

Satu pasien dapat memiliki banyak pendaftaran/kunjungan.

------------------------------------------------------------------------

# 21. URL Django

## Public

``` text
/daftar/
/checkin/
/antrian/<kode>/
```

## Admisi

``` text
/admisi/
/admisi/pasien/
/admisi/pendaftaran/
/admisi/antrian/
/admisi/checkin/
```

## Dokter

``` text
/dokter/
/dokter/antrian/
/dokter/periksa/<id>/
/dokter/riwayat/<pasien_id>/
```

------------------------------------------------------------------------

# 22. Dashboard

## Dashboard Admisi

Menampilkan:

-   Pasien terdaftar hari ini.
-   Pasien belum check-in.
-   Pasien menunggu.
-   Pasien dipanggil.
-   Pasien diperiksa.
-   Pasien selesai.

## Dashboard Dokter

Menampilkan:

-   Pasien menunggu.
-   Pasien dipanggil.
-   Pasien sedang diperiksa.
-   Pasien selesai hari ini.

------------------------------------------------------------------------

# 23. Alur Sistem Keseluruhan

``` text
             PASIEN
                │
       ┌────────┴─────────┐
       │                  │
  DAFTAR ONLINE      DATANG LANGSUNG
       │                  │
       │               ADMISI
       │                  │
       └────────┬─────────┘
                │
           PENDAFTARAN
                │
          STATUS TERDAFTAR
                │
       BELUM ADA ANTREAN
                │
        PASIEN SUDAH ONSITE
                │
       ┌────────┴────────┐
       │                 │
 QR CHECK-IN       CHECK-IN ADMISI
       │                 │
       └────────┬────────┘
                │
             CHECK-IN
                │
       GENERATE NO ANTREAN
                │
             MENUNGGU
                │
          PETUGAS PANGGIL
                │
            DIPANGGIL
                │
         DOKTER PERIKSA
                │
            DIPERIKSA
                │
       ┌────────┼────────┐
       │        │        │
   RIWAYAT    CPPT     RESEP
       │        │        │
       └────────┼────────┘
                │
              SELESAI
```

------------------------------------------------------------------------

# 24. Prinsip Utama Sistem

1.  Pendaftaran online tidak menentukan urutan antrean.
2.  Nomor antrean hanya diberikan setelah pasien onsite dan check-in.
3.  Urutan antrean mengikuti waktu check-in.
4.  Tersedia QR khusus pendaftaran mandiri.
5.  Tersedia QR khusus check-in.
6.  Petugas dapat melakukan check-in manual.
7.  Petugas dapat memanggil pasien.
8.  Dokter dapat melihat CPPT dan riwayat kunjungan sebelumnya.
9.  Dokter dapat membuat resep.
10. Pelayanan berakhir dengan status `SELESAI`.
11. Aplikasi dibangun menggunakan **Python Django + MySQL/MariaDB +
    Bootstrap + HTMX**.
