```markdown
# Non-profit Grant Finder Scraper (Starter)

What this project does
- Collects grants from public sources (APIs and scraped pages).
- Stores them in SQLite.
- Uses GPT-4o to summarize grant details and score compatibility with a nonprofit profile.

Quick-start
1. Create a `.env` file with:
   - OPENAI_API_KEY=sk-...
   - (optional) USER_AGENT="YourApp/1.0 (contact@example.org)"
2. Install:
   - `python -m pip install -r requirements.txt`
3. Run:
   - `python main.py --profile example_profile.json`
4. The DB `grants.db` will contain results; summarized matches will be printed.

Important legal & ethical reminders
- Obey `robots.txt` and site Terms of Service.
- Prefer official APIs (Grants.gov, Candid data, etc.) over scraping.
- Respect rate limits and do not overwhelm target servers.

Extending
- Add new API clients under `scraper/apis.py`.
- Add site-specific scrapers under `scraper/web_scraper.py`.
- Improve matching logic in `summarize_gpt.py`.

```