#!/usr/bin/env bash
set -euo pipefail

# push.sh — Hilfsskript zum Initialisieren eines Git-Repos und Pushen zu einem Remote
# Achtung: Dieses Skript erstellt kein GitHub-Repository. Entweder erstelle das Repo
# manuell auf GitHub (empfohlen) oder nutze die GitHub-CLI (`gh repo create`) bevor
# du das Skript ausführst.

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT_DIR"

# Prüfe ob git installiert ist
if ! command -v git >/dev/null 2>&1; then
  echo "Error: git ist nicht installiert. Installiere git und versuche es erneut." >&2
  exit 2
fi

# Wenn noch kein Git-Repo vorhanden ist, initialisieren
if [ ! -d .git ]; then
  echo "Initialisiere neues Git-Repository..."
  git init
  git branch -M main || true
else
  echo "Git-Repository vorhanden. Überspringe git init."
fi

# Füge alle Dateien hinzu (achte auf .gitignore)
git add .

# Commit (falls noch nichts committet wurde)
if git rev-parse --verify HEAD >/dev/null 2>&1; then
  echo "Es existiert bereits ein Commit. Überspringe initialen Commit."
else
  git commit -m "Initial commit: Portfolio site" || true
fi

# Bestimme Remote
REMOTE_URL="${REMOTE_URL-}"  # kann per ENV gesetzt werden
if [ -z "$REMOTE_URL" ]; then
  read -r -p "Bitte Remote-URL eingeben (z.B. git@github.com:USER/REPO.git oder https://github.com/USER/REPO.git): " REMOTE_URL
fi

# Setze Remote, falls noch nicht gesetzt
if git remote | grep -q "origin"; then
  echo "Remote 'origin' existiert bereits. Aktualisiere URL auf: $REMOTE_URL"
  git remote set-url origin "$REMOTE_URL"
else
  git remote add origin "$REMOTE_URL"
fi

# Push
echo "Pushe zu origin main..."
git push -u origin main

echo "Fertig. Wenn du ein GitHub-Repository erstellen möchtest, kannst du vorher 'gh repo create' nutzen." 

echo "Hinweis: Wenn du ein privates Repo möchtest, erstelle das Repo auf GitHub als private Repository oder verwende 'gh repo create --private'." 
