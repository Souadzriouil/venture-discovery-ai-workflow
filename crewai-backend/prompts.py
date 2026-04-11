QUERY_EXPANSION = """Generate exactly 7 focused web search queries for this topic:
Topic: "{focus_area}"

Return JSON array of strings only, no prose.
"""

SUMMARIZER = """Summarize this source in 3-4 lines and return strict JSON:
Input:
Title: {title}
Content: {content}
URL: {url}

Return:
{{"Title": "...", "Summary": "...", "URL": "..."}}
If content is missing or URL is unknown, return: SKIP
"""

VENTURE_IDEATION = """You are an AI venture ideation agent.
Using the article Title and Summary below, generate 1–3 unique startup ideas.

Rules for diversity:
- Each idea MUST be mutually distinct (no near-duplicates).
- Do NOT reuse the same brand/product name across ideas.
- Vary business models/targets (B2B SaaS, marketplace, infra/charging, analytics, fleet ops, battery lifecycle, financing/insurance, consumer app).
- The one-line "idea" should be a crisp concept name (not a brand).

Return strict JSON ONLY:
{{"ventures":[{{"id":1,"idea":"...","summary":"...","URL":"..."}}]}}

Input:
Title: {title}
Summary: {summary}
URL: {url}
"""

MARKET_ESTIMATE = """You are a market research analyst. Estimate:
- TAM (USD), SAM (USD), SOM (USD), CAGR (%), Strategic Fit (1–10)
Return strict JSON only:

{{
  "id": {id},
  "idea": "{idea}",
  "summary": "{summary}",
  "TAM": <number>,
  "SAM": <number>,
  "SOM": <number>,
  "CAGR": <number>,
  "strategic_fit": <number>,
  "URL": "{url}"
}}

Use credible but approximate values; numbers only (no commas/units).
"""

SOLUTION_INSIGHTS = """Expand this venture into a mini proposal. Return strict JSON merging the input plus:
"insights": {{
  "go_to_market": "...",
  "justification": "...",
  "value_proposition": "...",
  "features": ["...", "..."],
  "positioning": "...",
  "differentiation": "..."
}}
Input JSON:
{venture_json}
Return strict JSON only.
"""

WHITE_SPACE = """White-space analysis. Merge the input JSON and append:
"white_space_analysis": {{
  "market_gap": "...",
  "company_fit": "..."
}}
Consider top competitors and capability fit.

Input:
{venture_json}

Return strict JSON only.
"""
