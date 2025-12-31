#!/usr/bin/env bash
set -euo pipefail

# Generates cover_letter.pdf from cover_letter.html using wkhtmltopdf or headless Chrome/Chromium.
# Usage: ./scripts/generate_cover_letter_pdf.sh

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
HTML="$ROOT_DIR/cover_letter.html"
OUT="$ROOT_DIR/cover_letter.pdf"

if [ ! -f "$HTML" ]; then
  echo "Error: $HTML not found." >&2
  exit 2
fi

if command -v wkhtmltopdf >/dev/null 2>&1; then
  echo "Using wkhtmltopdf to generate $OUT"
  wkhtmltopdf "$HTML" "$OUT"
  exit 0
fi

if command -v google-chrome >/dev/null 2>&1; then
  echo "Using google-chrome headless to generate $OUT"
  google-chrome --headless --disable-gpu --print-to-pdf="$OUT" "file://$HTML"
  exit 0
fi

if command -v chromium-browser >/dev/null 2>&1; then
  echo "Using chromium-browser headless to generate $OUT"
  chromium-browser --headless --disable-gpu --print-to-pdf="$OUT" "file://$HTML"
  exit 0
fi

if command -v chromium >/dev/null 2>&1; then
  echo "Using chromium headless to generate $OUT"
  chromium --headless --disable-gpu --print-to-pdf="$OUT" "file://$HTML"
  exit 0
fi

echo "No supported PDF generator found. Install 'wkhtmltopdf' or Chrome/Chromium." >&2
exit 3
