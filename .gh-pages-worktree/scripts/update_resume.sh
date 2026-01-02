#!/usr/bin/env bash
set -euo pipefail

# update_resume.sh
# Regenerates resume.pdf and cover_letter.pdf (if generators available)
# and recreates site-publish.zip excluding VCS and node_modules.

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT_DIR"

echo "Running cover letter PDF generator..."
if [ -x "scripts/generate_cover_letter_pdf.sh" ]; then
  scripts/generate_cover_letter_pdf.sh
else
  echo "Warning: scripts/generate_cover_letter_pdf.sh not found or not executable" >&2
fi

echo "Running resume PDF generator..."
if [ -x "scripts/generate_pdf.sh" ]; then
  scripts/generate_pdf.sh
else
  echo "Warning: scripts/generate_pdf.sh not found or not executable" >&2
fi

echo "Recreating site-publish.zip (excluding .git, .github, node_modules)..."
zip -r site-publish.zip . -x "*.git*" ".git/*" "*/.git/*" ".github/*" "node_modules/*" "*/node_modules/*"

echo "Update complete. site-publish.zip refreshed." 
