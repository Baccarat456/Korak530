# main.py
import argparse
import json
from scraper import apis, web_scraper  # package-style import; ensure package layout or run from root
from db import init_db, upsert_grant, list_unscored, save_summary_and_score
from summarize_gpt import summarize_and_score
import os

def load_profile(path: str):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def run_searches(keywords: str, profile: dict):
    # API-first example
    try:
        results = apis.search_grants_gov(keywords, page=1, page_size=25)
    except Exception as e:
        print("Grants.gov API error:", e)
        results = []
    for g in results:
        upsert_grant(g)

    # Example scraping fallback: a hypothetical list page
    # Replace with actual sites and selectors you are allowed to scrape
    example_site = "https://example.org/grants/list"
    try:
        scraped = web_scraper.scrape_simple_list_page(example_site, selector=".grant-item")
        for g in scraped:
            upsert_grant(g)
    except Exception as e:
        print("Scraping example site failed (expected in template):", e)

def run_summarization(profile: dict, limit=20):
    items = list_unscored(limit)
    for it in items:
        # reconstruct minimal grant dict
        grant = {"id": it["id"], "title": it["title"], "url": it["url"], "raw": it["raw"]}
        res = summarize_and_score(grant, profile)
        save_summary_and_score(it["id"], res["summary"], res["score"])
        print(f"{it['title'][:80]} -> score {res['score']:.2f}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", required=True, help="Path to nonprofit profile JSON")
    parser.add_argument("--keywords", default="education community health", help="Search keywords")
    args = parser.parse_args()

    init_db()
    profile = load_profile(args.profile)
    run_searches(args.keywords, profile)
    run_summarization(profile, limit=50)

if __name__ == "__main__":
    main()