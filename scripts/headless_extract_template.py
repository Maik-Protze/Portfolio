#!/usr/bin/env python3
"""
Headless‑Browser‑Vorlage für E‑Mail‑Extraktion (Playwright).

Hinweis: Playwright muss installiert und initialisiert werden:

  pip install playwright
  playwright install

Dieses Skript ist eine Vorlage; es lädt Seiten per Playwright um JS‑gerenderte Inhalte zu erfassen.
"""
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright
import json
import re

ROOT = Path(__file__).resolve().parents[1]
TARGETS = ROOT / 'applications' / 'targets.json'

EMAIL_RE = re.compile(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}')


async def run_for_url(playwright, url):
    browser = await playwright.chromium.launch()
    page = await browser.new_page(user_agent='Mozilla/5.0')
    try:
        await page.goto(url, timeout=15000)
        content = await page.content()
        return content
    except Exception as e:
        return None
    finally:
        await browser.close()


async def main():
    if not TARGETS.exists():
        print('targets.json missing')
        return 1
    with TARGETS.open('r', encoding='utf-8') as fh:
        data = json.load(fh)

    async with async_playwright() as p:
        for entry in data[:10]:
            urls = [entry.get('contact_page'), entry.get('website')]
            for u in filter(None, urls):
                print('Visiting', u)
                content = await run_for_url(p, u)
                if not content:
                    continue
                emails = set(EMAIL_RE.findall(content))
                if emails:
                    print('Found emails on', u, emails)

    return 0


if __name__ == '__main__':
    asyncio.run(main())
