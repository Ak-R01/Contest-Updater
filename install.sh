#!/usr/bin/env bash
set -euo pipefail

APP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
UNIT_DIR="$HOME/.config/systemd/user"

# 1. Python environment
python3 -m venv "$APP_DIR/venv"
"$APP_DIR/venv/bin/pip" install --quiet -r "$APP_DIR/requirements.txt"

# 2. Credentials to be provided by user manually
if [ ! -f "$APP_DIR/credentials.json" ]; then
  echo "Missing credentials.json"
  echo "Download it from Google Cloud Console (OAuth client, Desktop app)"
  echo "and put it in $APP_DIR, then run this script again."
  exit 1
fi

# 3. First time login (opens a browser), only if there's no token yet
if [ ! -f "$APP_DIR/token.json" ]; then 
  echo "Running once to authorize with google..."
  (cd "$APP_DIR" && ./venv/bin/python calender.py)
fi

# 4. systemd units
mkdir -p "$UNIT_DIR"

cat > "$UNIT_DIR/contest-updater.service" <<EOF
[Unit]
Description=Sync Codeforces contests to Google Calendar

[Service]
Type=oneshot
WorkingDirectory=$APP_DIR
ExecStart=$APP_DIR/venv/bin/python calender.py
EOF

cat > "$UNIT_DIR/contest-updater.timer" <<EOF
[Unit]
Description=Run contest updater daily and at login

[Timer]
OnStartupSec=2min
OnUnitActiveSec=1d

[Install]
WantedBy=timers.target
EOF

systemctl --user daemon-reload
systemctl --user enable --now contest-updater.timer
echo "Installed, Check with: systemctl --user list-timers"


