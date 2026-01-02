#!/usr/bin/env python3
import json
import re
import ssl
import urllib.request
import urllib.error
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]
TARGETS = ROOT / 'applications' / 'targets.json'
BACKUP = ROOT / 'applications' / 'targets.json.pre_extract.bak'
CSV_OUT = ROOT / 'applications' / 'targets_extracted.csv'

EMAIL_RE = re.compile(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}')
SKIP_KEYS = ['no-reply', 'noreply', 'donotreply', 'do-not-reply']


def fetch(url, timeout=10):
    ctx = ssl.create_default_context()
    try:
        req = urllib.request.Request(url, headers={'User-Agent':'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=timeout, context=ctx) as resp:
            return resp.geturl(), resp.read().decode(errors='ignore')
    except Exception as e:
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
    if not TARGETS.exists():
        print(f"ERROR: {TARGETS} not found")
        return 1

    shutil.copy2(TARGETS, BACKUP)
    print(f"Backup created: {BACKUP}")

    with TARGETS.open('r', encoding='utf-8') as fh:
        data = json.load(fh)

    updated = 0
    rows = []
    for entry in data:
        name = entry.get('name')
        current = entry.get('contact_email')
        candidate_list = candidate_urls(entry)
        found = None
        found_url = None
        for url in candidate_list:
            real_url, text = fetch(url)
            if not text:
                continue
            emails = find_emails(text)
            if emails:
                # prefer non-generic addresses
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
        if not found:
            # if no emails found, check if page shows a contact form
            for url in candidate_list:
                _, text = fetch(url)
                if text and ('<form' in text.lower() or 'contact form' in text.lower()):
                    entry['contact_verified'] = entry.get('contact_verified') or 'form-only'
                    break
            rows.append((name, current or '', entry.get('contact_verified',''), entry.get('website','')))
            continue

        # update if new or different
        if current != found:
            entry['contact_email'] = found
            entry['contact_found_by'] = found_url
            entry['contact_verified'] = 'auto-found'
            updated += 1

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

    print(f"Extraction complete — updated {updated} entries. CSV: {CSV_OUT}")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
