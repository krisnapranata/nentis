# Nentis - Sistem Klinik Gigi

Sistem informasi klinik gigi berbasis **Django** untuk mengelola alur pelayanan pasien dari pendaftaran hingga selesai. Siap produksi via Docker, bisa diakses publik dengan HTTPS lewat Nginx Proxy Manager.

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
| Database   | MariaDB 10.6                     |
| Frontend   | Django Template + Bootstrap 5    |
| Interaksi  | HTMX                             |
| QR Code    | qrcode + Pillow                  |
| Deployment | Docker + Gunicorn + Nginx/NPM    |

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
├── deploy/           # Script setup mirror registry & deploy
├── Dockerfile
├── .dockerignore
├── docker-compose.yml           # db + web + nginx (standalone, port 80)
├── docker-compose.server.yml    # db + web (port 8002, tanpa nginx)
├── docker-compose.npm.yml       # overlay: gabungkan web ke jaringan NPM
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

## Konfigurasi (`.env`)

Semua nilai rahasia (SECRET_KEY, kredensial database, akun default) dibaca dari file `.env` yang tidak di-commit.

```bash
cp .env.example .env   # lalu isi nilainya
```

Contoh untuk produksi HTTPS di belakang Nginx Proxy Manager:

```env
SECRET_KEY=<string-acak-panjang>
DEBUG=False
ALLOWED_HOSTS=nentis.krisna-ai.web.id,103.102.15.44,localhost,127.0.0.1
DB_NAME=nentis
DB_USER=sik
DB_PASSWORD=<password-db-aman>
DB_HOST=db
DB_PORT=3306
MYSQL_ROOT_PASSWORD=<password-root-aman>
CSRF_TRUSTED_ORIGINS=https://nentis.krisna-ai.web.id
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
ADMIN_PASSWORD=<password-aman>
ADMISI_PASSWORD=<password-aman>
DOKTER_PASSWORD=<password-aman>
```

## Menjalankan dengan Docker

### Standalone (db + web + nginx) — untuk demo/lokal

```bash
cd nentis
docker compose up -d --build
```

Aplikasi tersedia di `http://localhost` (nginx port 80).

### Server dengan Nginx Proxy Manager (produksi)

`docker-compose.server.yml` menjalankan `db` + `web` (port 8002). Overlay
`docker-compose.npm.yml` memasukkan `web` ke jaringan `proxy_default`
sehingga NPM bisa forward ke `nentis_web:8002`:

```bash
docker compose -f docker-compose.server.yml -f docker-compose.npm.yml up -d --build
```

Lalu di UI Nginx Proxy Manager buat **Proxy Host**:

| Field                | Nilai                     |
|----------------------|---------------------------|
| Domain Names         | `nentis.krisna-ai.web.id` |
| Scheme               | `http`                    |
| Forward Hostname/IP  | `nentis_web`              |
| Forward Port         | `8002`                    |
| Block Exploits       | ON                        |
| Websockets Support   | ON                        |
| SSL                  | Let's Encrypt, Force SSL  |

Aplikasi tersedia di `https://nentis.krisna-ai.web.id`.

### Jika Docker Hub diblokir (production)

```bash
sudo bash deploy/setup-docker-mirror.sh   # pasang mirror.gcr.io
docker compose -f docker-compose.server.yml -f docker-compose.npm.yml up -d --build
```

Skrip `deploy/install.sh` menjalankan cekan `.env` + `docker compose up -d --build`:

```bash
sudo bash deploy/install.sh
```

`Dockerfile` menerima dua build-arg agar tidak perlu mengedit file saat
deploy di mesin berbeda:

```bash
docker compose -f docker-compose.server.yml build \
  --build-arg PYTHON_IMAGE=python:3.11-slim \
  --build-arg PIP_INDEX_URL=https://pypi.org/simple
```

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

Setelah menjalankan `seed_data`, akun default (kredensial berasal dari env, nilai default di `settings.py`):

| Role     | Username | Password   |
|----------|----------|------------|
| Admin    | admin    | admin123   |
| Admisi   | admisi   | admisi123  |
| Dokter   | dokter   | dokter123  |

## Troubleshooting

| Gejala | Penyebab | Perbaikan |
|--------|----------|-----------|
| 502 Bad Gateway dari NPM | NPM diset forward ke `127.0.0.1:8002` (localhost di dalam container NPM) | Forward ke `nentis_web:8002`, gabungkan `web` ke `proxy_default` via `docker-compose.npm.yml` |
| Login ditolak CSRF / pakai form HTTPS | `CSRF_TRUSTED_ORIGINS` / cookie secure belum diset | Tambahkan `CSRF_TRUSTED_ORIGINS`, `SESSION_COOKIE_SECURE=True`, `CSRF_COOKIE_SECURE=True` |
| DisallowedHost | `ALLOWED_HOSTS` tidak memuat domain | Isi `ALLOWED_HOSTS` dengan hostname yang diakses |
| `i/o timeout` saat build | Docker Hub diblokir | `sudo bash deploy/setup-docker-mirror.sh` |
| `Can't connect to MySQL` | `DB_HOST` salah | Pastikan `DB_HOST=db` (compose), `localhost` (langsung) |
| Suara tidak kedengaran | Browser memblokir Web Speech API di HTTP | Akses via HTTPS (secure context) |
