#!/usr/bin/env python3
"""
Bereinigt offensichtliche Falschtreffer aus `applications/targets.json` / `targets_extracted.csv`
und erzeugt `applications/top10_for_manual_review.csv` mit den 10 wichtigsten `auto-found` Treffern.

Usage: python3 scripts/clean_and_prepare.py
"""
import csv
import json
import re
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]
TARGETS = ROOT / 'applications' / 'targets.json'
EX_CSV = ROOT / 'applications' / 'targets_extracted.csv'
TOP10 = ROOT / 'applications' / 'top10_for_manual_review.csv'
BACKUP = ROOT / 'applications' / 'targets.json.pre_clean.bak'

INVALID_PATTERNS = [
    r"\.png$",
    r"Icon-?\d+@?2x?\.png",
    r"%20",
    r"support@yourcompany\.com",
    r"^Icon",
]

INVALID_RE = re.compile("|".join(f"({p})" for p in INVALID_PATTERNS), re.IGNORECASE)


def load_json():
    with TARGETS.open('r', encoding='utf-8') as fh:
        return json.load(fh)


def save_json(data):
    with TARGETS.open('w', encoding='utf-8') as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2)


def clean_entry(entry):
    email = entry.get('contact_email')
    if not email:
        return False
    if INVALID_RE.search(email) or ' ' in email:
        # record original
        note = entry.get('clean_note','')
        entry['clean_note'] = (note + '; ' if note else '') + f"removed:{email}"
        entry['contact_email'] = None
        entry['contact_verified'] = 'needs-check'
        # keep contact_found_by as reference
        return True
    return False


def main():
    if not TARGETS.exists():
        print('targets.json not found')
        return 1

    shutil.copy2(TARGETS, BACKUP)
    print(f'Backup: {BACKUP}')

    data = load_json()
    changed = 0
    for e in data:
        if clean_entry(e):
            changed += 1

    save_json(data)
    print(f'Bereinigung: {changed} Einträge angepasst')

    # Prepare Top10: choose entries with contact_verified == 'auto-found'
    auto = [e for e in data if e.get('contact_verified') == 'auto-found']
    # sort by distance if present
    auto_sorted = sorted(auto, key=lambda x: x.get('distance_km') if isinstance(x.get('distance_km'), (int,float)) else 9999)
    top10 = auto_sorted[:10]

    # write CSV
    with TOP10.open('w', encoding='utf-8', newline='') as cf:
        w = csv.writer(cf)
        w.writerow(['name','website','contact_email','contact_found_by','contact_verified','distance_km','clean_note'])
        for t in top10:
            w.writerow([
                t.get('name',''),
                t.get('website',''),
                t.get('contact_email',''),
                t.get('contact_found_by',''),
                t.get('contact_verified',''),
                t.get('distance_km',''),
                t.get('clean_note','')
            ])

    print(f'Erzeugt Top10 CSV: {TOP10} (Anzahl: {len(top10)})')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
