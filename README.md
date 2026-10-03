# Nentis - Sistem Klinik Gigi

Sistem informasi klinik gigi berbasis **Django** untuk mengelola alur pelayanan pasien dari pendaftaran hingga selesai.

## Alur Pelayanan

```
Pendaftaran (langsung dapat nomor antrean) → Antrean → Panggil → Pemeriksaan (CPPT/SOAP) → Resep → Selesai
```

## Fitur

- **Pendaftaran Mandiri** via QR Code — setelah daftar **langsung mendapat nomor antrean** (tanpa check-in terpisah)
- **Pencarian Pasien** — admisi dan halaman `/daftar/` bisa cari pasien lama berdasarkan nama, NIK, alamat, atau No. HP
- **Manajemen Antrean** real-time dengan HTMX (tanpa reload halaman)
- **Panggilan Bersuara** — saat pasien dipanggil, nama & nomor antrean diucapkan via Web Speech API
- **Pemeriksaan Dokter** dengan format SOAP (Subjective, Objective, Assessment, Plan)
- **Riwayat Kunjungan & CPPT** pasien
- **Resep Obat** dengan pencarian obat (typeahead) dan master data obat
- **Master Obat** — dikelola oleh admisi (tambah/ubah/hapus/nonaktifkan)
- **Odontogram** untuk pencatatan kondisi gigi
- **Dashboard** admisi dan dokter
- Multi-aktor: Pasien, Petugas Admisi, Dokter, Administrator

## Teknologi

| Komponen   | Teknologi                        |
|------------|----------------------------------|
| Backend    | Python 3.12 + Django 4.2         |
| Database   | MariaDB / MySQL                  |
| Frontend   | Django Template + Bootstrap 5    |
| Interaksi  | HTMX                             |
| QR Code    | qrcode + Pillow                  |
| Deployment | Docker + Gunicorn + Nginx        |

## Struktur Proyek

```
nentis/
├── accounts/         # Manajemen user & otentikasi (custom User + role)
├── antrian/          # Manajemen antrean & panggilan
├── config/           # Konfigurasi Django (settings, urls, wsgi)
├── dashboard/        # Redirect dashboard berdasarkan role
├── odontogram/       # Pencatatan odontogram gigi
├── pasien/           # Data pasien & pendaftaran mandiri
├── pendaftaran/      # Pendaftaran, pencarian pasien & master obat admisi
├── pemeriksaan/      # Pemeriksaan & CPPT dokter
├── resep/            # Resep obat & master obat
├── static/           # File statis (CSS, JS, gambar)
├── templates/        # Template HTML Django (project-level)
├── media/            # File upload (QR code, dll)
├── Dockerfile
├── docker-compose.yml          # db + web + nginx (standalone)
├── docker-compose.server.yml   # db + web saja (untuk server dengan reverse proxy)
├── nginx.conf
├── manage.py
└── requirements.txt
```

## Status Pelayanan

```
TERDAFTAR → MENUNGGU → DIPANGGIL → DIPERIKSA → SELESAI
```

**Catatan:** Pendaftaran **langsung** memberikan nomor antrean (check-in dilakukan otomatis saat daftar).

## Prasyarat

- [Docker](https://docs.docker.com/get-docker/) & [Docker Compose](https://docs.docker.com/compose/install/)
- Atau: Python 3.10+, MariaDB/MySQL, virtualenv

## Menjalankan dengan Docker

### Standalone (db + web + nginx)

```bash
cd nentis
docker compose up -d --build
```

Aplikasi tersedia di `http://localhost` (nginx port 80).

### Untuk server yang sudah punya reverse proxy (tanpa nginx)

Gunakan `docker-compose.server.yml` (db + web saja, web dipublish di port **8002**):

```bash
cd nentis
docker compose -f docker-compose.server.yml up -d --build
```

Aplikasi tersedia di `http://localhost:8002`.

## Menjalankan tanpa Docker

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Konfigurasi database via env: DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT
# (default di config/settings.py: nentis / sik / 00 / localhost / 3306)

python manage.py migrate
python manage.py seed_data
python manage.py runserver
```

## QR Code

| QR                 | URL        | Fungsi                                           |
|--------------------|------------|--------------------------------------------------|
| **Daftar Mandiri** | `/daftar/` | Cari pasien lama / daftar pasien baru + antrean  |

## URL Utama

| Halaman               | URL                          | Akses   |
|-----------------------|------------------------------|---------|
| Beranda (QR + Login)  | `/`                          | Public  |
| Daftar / Cari Pasien  | `/daftar/`                   | Public  |
| Display Antrean (TV)  | `/display/`                  | Public  |
| Login                 | `/accounts/login/`           | Public  |
| Dashboard Admisi      | `/admisi/`                   | Admisi  |
| Cari / Daftar Pasien  | `/admisi/pasien/`            | Admisi  |
| Antrean & Panggil     | `/admisi/antrian/`           | Admisi  |
| Master Obat           | `/admisi/master-obat/`       | Admisi  |
| Dashboard Dokter      | `/dokter/`                   | Dokter  |
| Antrean Dokter        | `/dokter/antrian/`           | Dokter  |
| Pemeriksaan           | `/dokter/periksa/<id>/`      | Dokter  |
| Resep                 | `/dokter/resep/<id>/`        | Dokter  |
| Riwayat Pasien        | `/dokter/riwayat/<id>/`      | Dokter  |

## Akun Default

Setelah menjalankan `seed_data`, akun default:

| Role     | Username | Password   |
|----------|----------|------------|
| Admin    | admin    | admin123   |
| Admisi   | admisi   | admisi123  |
| Dokter   | dokter   | dokter123  |
