# scraper/apis.py
import requests
import os
from typing import List, Dict
from time import sleep

# Example: simple Grants.gov API client (public search endpoint)
# NOTE: Confirm the actual Grants.gov API endpoints and parameters before production use.
GRANTS_GOV_ENDPOINT = "https://www.grants.gov/grantsws/rest/opportunities/search"

DEFAULT_HEADERS = {
    "Accept": "application/json",
    "User-Agent": os.getenv("USER_AGENT", "nonprofit-grant-finder/1.0 (+contact@example.org)"),
}

def search_grants_gov(keywords: str, page: int = 1, page_size: int = 25) -> List[Dict]:
    """
    Query Grants.gov search API. This is an example and may need parameter adjustments for the real API.
    Returns a list of normalized grant dicts.
    """
    params = {
        "Keyword": keywords,
        "p": page,
        "ps": page_size
    }
    resp = requests.get(GRANTS_GOV_ENDPOINT, params=params, headers=DEFAULT_HEADERS, timeout=15)
    resp.raise_for_status()
    data = resp.json()

    # Normalization: depends on API shape; adapt accordingly.
    results = []
    for item in data.get("opportunities", []):
        grant = {
            "id": f"grantsgov-{item.get('opportunityNumber') or item.get('id')}",
            "title": item.get("opportunityTitle") or item.get("title"),
            "source": "grants.gov",
            "url": item.get("url") or item.get("opportunityUrl"),
            "posted_date": item.get("postedDate"),
            "deadline": item.get("closeDate"),
            "raw": item
        }
        results.append(grant)
    # polite pause
    sleep(0.5)
    return results