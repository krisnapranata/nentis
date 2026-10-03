#!/usr/bin/env bash
# Pasang registry-mirror untuk Docker Hub (dijalankan dengan sudo).
# Idempotent: merge ke daemon.json yang ada, backup otomatis.
set -euo pipefail

DAEMON_JSON=/etc/docker/daemon.json
MIRROR_URL="${1:-https://mirror.gcr.io}"

if [[ $EUID -ne 0 ]]; then
  echo "Jalankan dengan sudo: sudo $0"
  exit 1
fi

mkdir -p /etc/docker

if [[ -f "$DAEMON_JSON" ]]; then
  cp "$DAEMON_JSON" "${DAEMON_JSON}.bak.$(date +%Y%m%d%H%M%S)"
fi

python3 - "$DAEMON_JSON" "$MIRROR_URL" <<'PY'
import json, sys, pathlib
path = pathlib.Path(sys.argv[1])
mirror = sys.argv[2]
try:
    data = json.loads(path.read_text()) if path.exists() else {}
except json.JSONDecodeError:
    data = {}
mirrors = data.setdefault("registry-mirrors", [])
if mirror not in mirrors:
    mirrors.append(mirror)
path.write_text(json.dumps(data, indent=2) + "\n")
print(json.dumps(data, indent=2))
PY

systemctl daemon-reload
systemctl restart docker

echo
echo "Registry mirrors aktif:"
docker info 2>/dev/null | grep -iA4 'Registry Mirrors' || true
echo
echo "Verifikasi dengan: docker pull python:3.12-slim"
