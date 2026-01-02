#!/usr/bin/env python3
import json
import shutil
from pathlib import Path
import csv

ROOT = Path(__file__).resolve().parents[1]
TARGETS = ROOT / 'applications' / 'targets.json'
BACKUP = ROOT / 'applications' / 'targets.json.bak'
CSV_OUT = ROOT / 'applications' / 'targets.csv'


def main():
    if not TARGETS.exists():
        print(f"ERROR: {TARGETS} not found")
        return 1

    # Backup
    shutil.copy2(TARGETS, BACKUP)
    print(f"Backup created: {BACKUP}")

    # Load JSON
    with TARGETS.open('r', encoding='utf-8') as fh:
        data = json.load(fh)

    # Add contact_verified where missing
    changed = 0
    for entry in data:
        if 'contact_verified' not in entry or entry.get('contact_verified') in (None, ''):
            if entry.get('contact_email'):
                entry['contact_verified'] = 'confirmed'
            else:
                entry['contact_verified'] = 'needs-check'
            changed += 1

    # Write back JSON (pretty)
    with TARGETS.open('w', encoding='utf-8') as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2)

    print(f"Updated {TARGETS} — set contact_verified on {changed} entries")

    # Generate CSV
    headers = ['name', 'contact_email', 'contact_verified', 'website']
    with CSV_OUT.open('w', encoding='utf-8', newline='') as csvf:
        writer = csv.writer(csvf)
        writer.writerow(headers)
        for entry in data:
            writer.writerow([
                entry.get('name',''),
                entry.get('contact_email',''),
                entry.get('contact_verified',''),
                entry.get('website','')
            ])

    print(f"Wrote CSV: {CSV_OUT}")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
