#!/usr/bin/env bash
set -euo pipefail

# transfer_to_notebook.sh
# Verwendung: ./scripts/transfer_to_notebook.sh user@host [/remote/path]
# Überträgt das neueste Backup‑Verzeichnis (erstellt mit backup_vscode.sh) per rsync zum Remote‑Host.

if [ "$#" -lt 1 ]; then
  echo "Verwendung: $0 user@host [remote_path]"
  exit 1
fi

REMOTE="$1"
REMOTE_PATH="${2:-~/vscode-backup-remote}"

BACKUP_DIR_PATTERN="$HOME/vscode-backup-*"
LATEST_BACKUP=$(ls -dt $BACKUP_DIR_PATTERN 2>/dev/null | head -n1 || true)

if [ -z "$LATEST_BACKUP" ]; then
  echo "Kein Backup‑Verzeichnis gefunden. Bitte zuerst scripts/backup_vscode.sh ausführen." >&2
  exit 2
fi

echo "Übertrage $LATEST_BACKUP nach $REMOTE:$REMOTE_PATH"

# Nutze rsync für zuverlässige Übertragung
rsync -avz --progress --omit-dir-times --no-perms "$LATEST_BACKUP/" "$REMOTE":"$REMOTE_PATH/"

echo "Übertragung abgeschlossen. Prüfe auf Remote: ssh $REMOTE ls -la $REMOTE_PATH"
