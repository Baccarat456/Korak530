# scraper/web_scraper.py
import requests
from bs4 import BeautifulSoup
import os
from time import sleep
from typing import List, Dict
import hashlib

DEFAULT_HEADERS = {
    "User-Agent": os.getenv("USER_AGENT", "nonprofit-grant-finder/1.0 (+contact@example.org)")
}

def _id_from_url(url: str) -> str:
    h = hashlib.sha1(url.encode("utf-8")).hexdigest()
    return f"page-{h}"

def scrape_simple_list_page(url: str, selector: str, title_selector: str = None, link_selector: str = None) -> List[Dict]:
    """
    Generic scraper for pages that list grants as links.
    - selector: CSS selector for each item block (e.g., '.result-item')
    - title_selector: CSS selector relative to item for title (defaults to link text)
    - link_selector: CSS selector relative to item for link (defaults to 'a')
    Returns normalized grant dicts.
    """
    resp = requests.get(url, headers=DEFAULT_HEADERS, timeout=15)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    items = soup.select(selector)
    out = []
    for item in items:
        a = item.select_one(link_selector or "a")
        if not a or not a.get("href"):
            continue
        link = requests.compat.urljoin(url, a["href"])
        title_el = item.select_one(title_selector) if title_selector else a
        title = title_el.get_text(strip=True) if title_el else a.get_text(strip=True)
        gid = _id_from_url(link)
        grant = {
            "id": gid,
            "title": title,
            "source": url.split("//", 1)[-1].split("/", 1)[0],
            "url": link,
            "posted_date": None,
            "deadline": None,
            "raw": {"page_snippet": str(item)[:2000]}
        }
        out.append(grant)
    # polite pause
    sleep(1.0)
    return out

# Example more advanced scraping (JS heavy) can use Playwright / Selenium — omitted for brevity.