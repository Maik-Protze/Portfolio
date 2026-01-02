#!/usr/bin/env python3
"""
Extract emails for the next N unconfirmed entries in `applications/targets.json`.

Usage: python3 scripts/extract_next_n.py [N]
Default N=20
"""
import json
import re
import ssl
import sys
import urllib.request
import urllib.error
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]
TARGETS = ROOT / 'applications' / 'targets.json'
BACKUP = ROOT / 'applications' / 'targets.json.pre_next20.bak'
CSV_OUT = ROOT / 'applications' / 'targets_next20_extracted.csv'

EMAIL_RE = re.compile(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}')
SKIP_KEYS = ['no-reply', 'noreply', 'donotreply', 'do-not-reply']


def fetch(url, timeout=10):
    ctx = ssl.create_default_context()
    try:
        req = urllib.request.Request(url, headers={'User-Agent':'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=timeout, context=ctx) as resp:
            return resp.geturl(), resp.read().decode(errors='ignore')
    except Exception:
        return None, None


def find_emails(text):
    if not text:
        return []
    matches = EMAIL_RE.findall(text)
    out = []
    for m in matches:
        low = m.lower()
        if any(k in low for k in SKIP_KEYS):
            continue
        if m not in out:
            out.append(m)
    return out


def candidate_urls(entry):
    urls = []
    if entry.get('contact_page'):
        urls.append(entry['contact_page'])
    site = entry.get('website')
    if site:
        site = site.rstrip('/')
        urls.extend([
            site,
            site + '/kontakt',
            site + '/kontakt/',
            site + '/contact',
            site + '/contact/',
            site + '/impressum',
            site + '/impressum/',
        ])
    return urls


def main():
    n = 20
    if len(sys.argv) > 1:
        try:
            n = int(sys.argv[1])
        except Exception:
            pass

    if not TARGETS.exists():
        print(f"ERROR: {TARGETS} not found")
        return 1

    shutil.copy2(TARGETS, BACKUP)
    print(f"Backup created: {BACKUP}")

    with TARGETS.open('r', encoding='utf-8') as fh:
        data = json.load(fh)

    # select next N entries where contact_verified != 'confirmed'
    pending = [e for e in data if e.get('contact_verified') != 'confirmed']
    to_process = pending[:n]

    rows = []
    updated = 0
    for entry in to_process:
        name = entry.get('name')
        current = entry.get('contact_email')
        found = None
        found_url = None
        for url in candidate_urls(entry):
            real_url, text = fetch(url)
            if not text:
                continue
            emails = find_emails(text)
            if emails:
                # pick first non-generic if possible
                pref = None
                for e in emails:
                    low = e.lower()
                    if 'info@' in low or 'kontakt@' in low or 'service@' in low:
                        continue
                    pref = e
                    break
                if not pref:
                    pref = emails[0]
                found = pref
                found_url = real_url or url
                break
        if found:
            if current != found:
                entry['contact_email'] = found
                entry['contact_found_by'] = found_url
                entry['contact_verified'] = 'auto-found'
                updated += 1
        else:
            # if no found, check for contact form presence
            for url in candidate_urls(entry):
                _, text = fetch(url)
                if text and ('<form' in text.lower() or 'contact form' in text.lower()):
                    entry['contact_verified'] = entry.get('contact_verified') or 'form-only'
                    break

        rows.append((name, entry.get('contact_email',''), entry.get('contact_verified',''), entry.get('website',''), entry.get('contact_found_by','')))

    # write back
    with TARGETS.open('w', encoding='utf-8') as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2)

    # write CSV
    import csv
    with CSV_OUT.open('w', encoding='utf-8', newline='') as cf:
        w = csv.writer(cf)
        w.writerow(['name','contact_email','contact_verified','website','contact_found_by'])
        for r in rows:
            w.writerow(list(r))

    print(f"Processed {len(to_process)} entries — updated {updated}. CSV: {CSV_OUT}")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
