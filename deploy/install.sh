#!/usr/bin/env bash
# Deploy nentis (db + web) di server. Jalankan dari folder repo.
set -euo pipefail

cd "$(dirname "$0")/.."

if ! command -v docker >/dev/null 2>&1; then
  echo "Docker belum terpasang."
  exit 1
fi

if [[ ! -f .env ]]; then
  echo ".env belum ada. Salin dari .env.example lalu isi."
  cp .env.example .env
  echo "Edit .env terlebih dahulu, lalu jalankan lagi."
  exit 1
fi

docker compose -f docker-compose.server.yml config --quiet
docker compose -f docker-compose.server.yml up -d --build

echo
echo "Menunggu container siap..."
sleep 20
docker compose -f docker-compose.server.yml ps

APP_URL="http://$(hostname -I 2>/dev/null | awk '{print $1}'):8002"
echo
echo "Selesai. Aplikasi dapat diakses di: $APP_URL"
