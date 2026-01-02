#!/usr/bin/env bash
set -euo pipefail

# restore_vscode.sh
# Verwendung: ./scripts/restore_vscode.sh /path/to/backup_dir
# Entpackt die Sicherungen und kopiert VS Code Einstellungen zurück nach ~/.config/Code/User

if [ "$#" -lt 1 ]; then
  echo "Verwendung: $0 /pfad/zum/backup_verzeichnis"
  exit 1
fi

BACKUP_DIR="$1"

if [ ! -d "$BACKUP_DIR" ]; then
  echo "Backup-Verzeichnis nicht gefunden: $BACKUP_DIR" >&2
  exit 2
fi

echo "Entpacke und stelle wieder her aus: $BACKUP_DIR"

# 1) Entpacke vscode-user.tgz falls vorhanden
if [ -f "$BACKUP_DIR/vscode-user.tgz" ]; then
  tar -xzf "$BACKUP_DIR/vscode-user.tgz" -C ~/
  echo "Entpackt: vscode-user.tgz"
fi

# 2) Kopiere Benutzer‑Einstellungen
if [ -d "$BACKUP_DIR/user-settings" ]; then
  mkdir -p ~/.config/Code/User
  cp -a "$BACKUP_DIR/user-settings/"* ~/.config/Code/User/
  echo "Benutzer‑Einstellungen nach ~/.config/Code/User/ kopiert"
fi

# 3) Installiere Erweiterungen (falls extensions.txt vorhanden)
if [ -f "$BACKUP_DIR/extensions.txt" ]; then
  if command -v code >/dev/null 2>&1; then
    cat "$BACKUP_DIR/extensions.txt" | xargs -L 1 code --install-extension || true
    echo "Erweiterungen installiert (sofern 'code' verfügbar)"
  else
    echo "VS Code CLI 'code' nicht gefunden. Erweiterungen können nicht automatisch installiert werden." >&2
  fi
fi

echo "Wiederherstellung abgeschlossen. Starte VS Code und überprüfe Einstellungen und Erweiterungen."
