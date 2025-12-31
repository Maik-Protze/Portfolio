#!/usr/bin/env bash
set -euo pipefail

# remove_old_email.sh
# Removes occurrences of the old email from site files and rebuilds site-publish.zip
# Usage: ./scripts/remove_old_email.sh

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT_DIR"

OLD_EMAIL="maik.protze@student-dci.org"
# Remove visible old email mentions from the files
FILES=(index.html resume.html cover_letter.html)
for f in "${FILES[@]}"; do
  if [ -f "$f" ]; then
    cp "$f" "$f.bak"
    # remove alt mention
    sed -i "s| (alt: ${OLD_EMAIL}, will be removed on 01.03.2026)||g" "$f" || true
    sed -i "s| (alt: ${OLD_EMAIL}, wird 01.03.2026 entfernt)||g" "$f" || true
    sed -i "s|${OLD_EMAIL}||g" "$f" || true
  fi
done

# Also replace any mailto that still points to old email
sed -i "s|mailto:${OLD_EMAIL}|mailto:maik.p11@web.de|g" index.html || true

# Recreate site zip
zip -r site-publish.zip . -x "*.git*" ".git/*" "*/.git/*" ".github/*" "node_modules/*" "*/node_modules/*"

echo "Old email removed and site-publish.zip updated." 
