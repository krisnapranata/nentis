# AGENTS.md

Django 4.2 + MySQL/MariaDB app for a dental clinic (Indonesian). No git repo, no
lint/typecheck config, no frontend build step. Bootstrap + HTMX are loaded from
CDN in `templates/base.html`.

## Commands

Use the bundled venv (`./venv/bin/python`); do not assume a global Python.

```bash
./venv/bin/python manage.py check                  # quick validation (no DB writes)
./venv/bin/python manage.py makemigrations <app>   # after model changes
./venv/bin/python manage.py migrate
./venv/bin/python manage.py seed_data              # creates default users + master obat
./venv/bin/python manage.py runserver              # dev server (default :8000)
```

- `seed_data` creates: `admin/admin123`, `admisi/admisi123`, `dokter/dokter123`.
  README's "Akun Default" table (admin/admin, etc.) is **stale** — trust seed_data.
  Usernames/passwords come from env (`ADMIN_USERNAME`/`ADMIN_PASSWORD`, etc.).
- Secrets (SECRET_KEY, DB creds, seed users) are read from `.env` via
  `python-dotenv` in `config/settings.py`. `.env` is gitignored; see `.env.example`.
  Keep these in env, never hardcode.
- Tests are empty placeholders (`* /tests.py` contain only `pass`-style stubs).
  `manage.py test` needs a MySQL test database and will likely fail without
  CREATE DATABASE privileges — verify behavior manually or via the shell instead.

## Database

MySQL/MariaDB, not SQLite. Connection comes from env vars (`DB_NAME`, `DB_USER`,
`DB_PASSWORD`, `DB_HOST`, `DB_PORT`), defaults hard-coded in `config/settings.py`
as `nentis` / `sik` / `00` / `localhost` / `3306`. `docker compose up -d` runs
`migrate` + `seed_data` automatically.

## Architecture

- Custom user model `accounts.User` with a `role` CharField:
  `admin | admisi | dokter | pasien`. Access control is done via per-view
  `user_passes_test` with local `is_admisi` / `is_dokter` / `is_petugas`
  helpers (each app redefines them) and `login_url='/accounts/login/'`.
- Root URLs in `config/urls.py` route by role namespace, all `include`d:
  - `/` → `pasien.urls` (public: landing QR page, `/daftar/`, `/checkin/`)
  - `/admisi/` → `pendaftaran.urls` + `antrian.urls_admisi` + `resep.urls_admisi`
  - `/dokter/` → `pemeriksaan.urls` + `antrian.urls_dokter` + `resep.urls` + `odontogram.urls`
  - `/accounts/` → login/logout; `/dashboard/` redirects by role; `/display/` → queue TV screen
- Templates are project-level in `/templates` (shared `base.html`), **except**
  `odontogram/` which keeps its own `templates/` and `templatetags/` dirs.
- Queue/status flow: `TERDAFTAR → MENUNGGU → DIPANGGIL → DIPERIKSA → SELESAI`.

## Non-obvious behavior

- Public registration (`/daftar/`, view `pasien.views.daftar`) **auto-checks-in**
  and assigns a queue number immediately (the separate check-in step was removed).
- `antrian.views.panggil_antrian` serves **both** admisi and dokter, allows
  re-calling (`status__in=['MENUNGGU','DIPANGGIL']`), and returns a **different
  partial** per role when the request has `HX-Request`: `pendaftaran/_antrian_rows.html`
  for admisi, `antrian/_dokter_menunggu_rows.html` for dokter. Keep these in sync.
- Patient call plays voice via Web Speech API (`speechSynthesis`, `id-ID`) in the
  queue templates and the `/display/` page — this is client-side JS, not Django.
- Resep (doctor's prescription) uses a typeahead on the `MasterObat` field
  (min 3 chars) hitting `dokter/resep/cari-obat/`. `MasterObat` is only
  addable/editable by admisi/admin via `/admisi/master-obat/`.
- Dates use `timezone.localtime(timezone.now()).date()` (settings TZ is
  `Asia/Makassar`); do not use `date.today()`.

## Domain reference

`nentis.txt` and `spesifikasi_sistem_klinik_gigi_django.md` (Indonesian) document
business rules (e.g. `KeadaanKhusus` for pregnancy/hypertension/allergies). Read
them before changing flows.
