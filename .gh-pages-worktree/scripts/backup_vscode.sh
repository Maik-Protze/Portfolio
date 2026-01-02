#!/usr/bin/env bash
set -euo pipefail

# backup_vscode.sh
# Verwendung: ./scripts/backup_vscode.sh [--include-ssh] [--projects DIR1,DIR2,...]
# Legt einen Backup-Ordner in $HOME/vscode-backup-YYYY-MM-DD an mit:
# - VS Code Benutzer‑Einstellungen (settings.json, keybindings, snippets)
# - Liste der installierten Erweiterungen (extensions.txt)
# - Archiv von .vscode und .vscode-server (falls vorhanden)
# - optionale Projekt‑Archive

BACKUP_DIR="$HOME/vscode-backup-$(date +%F)"
mkdir -p "$BACKUP_DIR"

INCLUDE_SSH=false
PROJECTS_TO_ARCHIVE=()

while [ "$#" -gt 0 ]; do
  case "$1" in
    --include-ssh)
      INCLUDE_SSH=true; shift;;
    --projects)
      shift
      IFS=',' read -r -a PROJECTS_TO_ARCHIVE <<< "$1"
      shift;;
    --help|-h)
      sed -n '1,200p' "$0"; exit 0;;
    *)
      echo "Unknown arg: $1"; exit 1;;
  esac
done

echo "Erstelle Backup in: $BACKUP_DIR"

# 1) User settings
USER_SETTINGS_DEST="$BACKUP_DIR/user-settings"
mkdir -p "$USER_SETTINGS_DEST"

if [ -d "$HOME/.config/Code/User" ]; then
  cp -a "$HOME/.config/Code/User" "$USER_SETTINGS_DEST/"
  echo "Kopiert: ~/.config/Code/User"
elif [ -d "$HOME/.vscode-server/data/Machine/User" ]; then
  cp -a "$HOME/.vscode-server/data/Machine/User" "$USER_SETTINGS_DEST/"
  echo "Kopiert: ~/.vscode-server/data/Machine/User"
else
  echo "Keine VS Code Benutzer‑Einstellungsordner an bekannten Orten gefunden." >&2
fi

# 2) Extensions list
if command -v code >/dev/null 2>&1; then
  code --list-extensions > "$BACKUP_DIR/extensions.txt" || true
  echo "Erzeugte Liste der Erweiterungen: $BACKUP_DIR/extensions.txt"
else
  echo "VS Code 'code' CLI not found. Skipping extensions list." >&2
fi

# 3) Archive .vscode and .vscode-server if present
if [ -d "$HOME/.vscode" ]; then
  tar -czf "$BACKUP_DIR/vscode-user.tgz" -C "$HOME" ".vscode" || true
  echo "Archiv erstellt: ~/.vscode -> $BACKUP_DIR/vscode-user.tgz"
fi
if [ -d "$HOME/.vscode-server" ]; then
  tar -czf "$BACKUP_DIR/vscode-server.tgz" -C "$HOME" ".vscode-server" || true
  echo "Archiv erstellt: ~/.vscode-server -> $BACKUP_DIR/vscode-server.tgz"
fi

# 4) Optional: SSH keys
if [ "$INCLUDE_SSH" = true ]; then
  if [ -d "$HOME/.ssh" ]; then
    tar -czf "$BACKUP_DIR/ssh-keys.tgz" -C "$HOME" ".ssh" || true
    echo "SSH‑Schlüssel eingeschlossen: $BACKUP_DIR/ssh-keys.tgz"
  else
    echo "Kein ~/.ssh Verzeichnis gefunden; SSH‑Backup übersprungen." >&2
  fi
fi

# 5) Archive projects provided by user
for p in "${PROJECTS_TO_ARCHIVE[@]}"; do
  if [ -d "$p" ]; then
    base=$(basename "$p")
    # exclude node_modules by default
    tar --exclude='**/node_modules' -czf "$BACKUP_DIR/${base}.tgz" -C "$p" . || true
    echo "Projektsicherung: $p -> $BACKUP_DIR/${base}.tgz"
  else
    echo "Projektpfad nicht gefunden: $p" >&2
  fi
done

echo "Backup abgeschlossen. Dateien in $BACKUP_DIR:"
ls -la "$BACKUP_DIR"

echo "Nächster Schritt: Übertrage das Backup mit scripts/transfer_to_notebook.sh oder per scp/rsync auf dein Notebook."
