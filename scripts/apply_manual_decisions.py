#!/usr/bin/env python3
"""
Apply manual decisions from the Top10 review:
- Set `contact_verified = 'confirmed'` for OK entries
- For entries marked PK (prüfen), attempt to find a better HR/jobs contact

Usage: python3 scripts/apply_manual_decisions.py
"""
import json
import re
import ssl
import urllib.request
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]
TARGETS = ROOT / 'applications' / 'targets.json'
BACKUP = ROOT / 'applications' / 'targets.json.pre_manual.bak'

def fetch_text(url, timeout=10):
    ctx = ssl.create_default_context()
    try:
        req = urllib.request.Request(url, headers={'User-Agent':'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=timeout, context=ctx) as resp:
            return resp.read().decode(errors='ignore')
    except Exception:
        return ''

EMAIL_RE = re.compile(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}')
HR_KEYWORDS = ['hr', 'career', 'recruit', 'jobs', 'bewerb', 'personal', 'karriere']


def find_hr_email(text):
    emails = EMAIL_RE.findall(text or '')
    candidates = []
    for e in emails:
        low = e.lower()
        for k in HR_KEYWORDS:
            if k in low:
                candidates.append(e)
                break
    return candidates


def main():
    if not TARGETS.exists():
        print('targets.json not found')
        return 1

    shutil.copy2(TARGETS, BACKUP)
    print(f'Backup created: {BACKUP}')

    with TARGETS.open('r', encoding='utf-8') as fh:
        data = json.load(fh)

    # Mapping from top10 entries (by name) to action
    decisions = {
        'Bennewitz / Böhlitz municipal office': 'confirm',
        'Netresearch DTT GmbH': 'confirm',
        'comspace GmbH': 'confirm',
        'HTWK Leipzig – Hochschule für Technik, Wirtschaft und Kultur': 'confirm',
        'MDR Sachsen (Mitteldeutscher Rundfunk)': 'confirm',
        'Tapio': 'prüfen',
        'Web-Pflege.com': 'confirm',
        'i-fabrik GmbH': 'confirm',
        'Universität Leipzig – IT-Services': 'confirm',
        'Leipziger Volkszeitung (LVZ)': 'confirm',
    }

    updated = 0
    for entry in data:
        name = entry.get('name')
        action = decisions.get(name)
        if not action:
            continue
        if action == 'confirm':
            entry['contact_verified'] = 'confirmed'
            updated += 1
        elif action == 'prüfen':
            # try to find HR/contact page with HR-like emails
            urls = []
            if entry.get('contact_page'):
                urls.append(entry['contact_page'])
            if entry.get('website'):
                site = entry.get('website').rstrip('/')
                urls += [site, site + '/career', site + '/careers', site + '/karriere', site + '/jobs', site + '/kontakt']
            found = None
            found_from = None
            for u in urls:
                txt = fetch_text(u)
                if not txt:
                    continue
                cands = find_hr_email(txt)
                if cands:
                    found = cands[0]
                    found_from = u
                    break
            if found:
                entry['contact_email'] = found
                entry['contact_verified'] = 'confirmed'
                entry['contact_found_by'] = found_from
                updated += 1
            else:
                # mark as needs-check (no HR found)
                entry['contact_verified'] = 'needs-check'

    with TARGETS.open('w', encoding='utf-8') as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2)

    print(f'Applied decisions. Entries updated: {updated}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
