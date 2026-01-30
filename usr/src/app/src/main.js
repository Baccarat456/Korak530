# summarize_gpt.py
import os
import time
from typing import Dict, Any
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

MODEL = "gpt-4o"  # your desired model name; check OpenAI docs and replace if needed

def summarize_and_score(grant: Dict[str, Any], profile: Dict[str, Any]) -> Dict[str, Any]:
    """
    Send a prompt to GPT-4o to:
     - produce a short summary of the grant (3-4 sentences)
     - estimate a compatibility score 0-1 for the given nonprofit profile
     - list up to 3 quick eligibility flags (red/yellow/green)
    Returns {'summary': str, 'score': float, 'flags': {...}}
    """
    prompt = f"""
You are an assistant that reads grant announcements and matches them to a nonprofit's profile.

Nonprofit profile (JSON):
{profile}

Grant raw data / page snippet (JSON-like or text):
{grant.get('raw')}

Please respond with a JSON object:
{{
  "summary": "<3-4 sentence plain English summary of the grant, who it's for, funding size if mentioned>",
  "score": 0.0,
  "flags": {{
      "geography": "green|yellow|red",
      "mission_fit": "green|yellow|red",
      "deadline_ok": "green|yellow|red"
  }},
  "notes": "<optional short notes>"
}}
Only return valid JSON.
"""
    # call OpenAI
    # Add basic retry/backoff
    for attempt in range(3):
        try:
            resp = openai.ChatCompletion.create(
                model=MODEL,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.0,
                max_tokens=500
            )
            text = resp["choices"][0]["message"]["content"]
            # parse JSON safely
            import json
            parsed = json.loads(text)
            # Ensure numeric score
            score = float(parsed.get("score") or 0.0)
            return {"summary": parsed.get("summary", ""), "score": score, "flags": parsed.get("flags", {}), "notes": parsed.get("notes", "")}
        except Exception as e:
            wait = 2 ** attempt
            time.sleep(wait)
    # fallback if GPT fails
    return {"summary": "", "score": 0.0, "flags": {}, "notes": "summarization failed"}
