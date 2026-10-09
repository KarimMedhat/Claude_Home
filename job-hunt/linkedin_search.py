"""Daily Job Hunt: LinkedIn public job search, last 48 hours.

Prints a JSON list of senior product / UI-UX design roles posted in the last
48 hours: remote or hybrid in Egypt, remote in the Gulf.

Usage: python3 job-hunt/linkedin_search.py
"""
import html
import json
import re
import sys
import time
import urllib.parse
import urllib.request

SEARCH = "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search"
LAST_48H = "r172800"
REMOTE, HYBRID = "2", "3"

KEYWORDS = [
    "Senior Product Designer",
    "Lead Product Designer",
    "Senior UI UX Designer",
    "Senior UX Designer",
    "Senior UI Designer",
]
# (location, country label, allowed work modes)
LOCATIONS = [
    ("Egypt", "Egypt", [REMOTE, HYBRID]),
    ("Saudi Arabia", "Saudi Arabia", [REMOTE]),
    ("United Arab Emirates", "UAE", [REMOTE]),
    ("Qatar", "Qatar", [REMOTE]),
    ("Kuwait", "Kuwait", [REMOTE]),
    ("Bahrain", "Bahrain", [REMOTE]),
    ("Oman", "Oman", [REMOTE]),
]
MODE_LABEL = {REMOTE: "Remote", HYBRID: "Hybrid"}

SENIOR = re.compile(r"\b(senior|sr\.?|lead|principal|staff)\b", re.I)
DESIGN = re.compile(r"(product design|\bui\b|\bux\b|ui/ux|ux/ui|user experience|user interface|experience design)", re.I)
EXCLUDE = re.compile(r"(graphic|motion|developer|engineer|researcher|writer|intern|junior)", re.I)
TRACK_PRODUCT = re.compile(r"product design", re.I)


def fetch(params):
    url = SEARCH + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0", "Accept-Language": "en-US,en;q=0.9"})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=25) as r:
                return r.read().decode("utf-8", "replace")
        except Exception as e:  # 429 / transient network errors
            print(f"warn: {params['keywords']} / {params['location']}: {e}", file=sys.stderr)
            time.sleep(4 * (attempt + 1))
    return ""


def field(pattern, text):
    m = re.search(pattern, text, re.S)
    return html.unescape(m.group(1)).strip() if m else ""


def parse(page):
    for card in page.split("<li>")[1:]:
        link = re.search(r'href="(https://[a-z]+\.linkedin\.com/jobs/view/[^"?]+)', card)
        dt = re.search(r'datetime="([^"]+)"[^>]*>\s*(.*?)\s*<', card, re.S)
        yield {
            "title": field(r'base-search-card__title">\s*(.*?)\s*<', card),
            "company": field(r'hidden-nested-link[^>]*>\s*(.*?)\s*<', card),
            "location": field(r'job-search-card__location">\s*(.*?)\s*<', card),
            "postedDate": dt.group(1) if dt else "",
            "postedText": dt.group(2).strip() if dt else "",
            "url": urllib.parse.unquote(link.group(1)) if link else "",
        }


def main():
    seen, results = set(), []
    for loc, country, modes in LOCATIONS:
        for mode in modes:
            for kw in KEYWORDS:
                page = fetch({"keywords": kw, "location": loc, "f_TPR": LAST_48H, "f_WT": mode, "start": 0})
                for job in parse(page):
                    jid = re.search(r"-(\d+)$", job["url"])
                    key = jid.group(1) if jid else job["url"]
                    if not job["title"] or key in seen:
                        continue
                    if not (SENIOR.search(job["title"]) and DESIGN.search(job["title"])) or EXCLUDE.search(job["title"]):
                        continue
                    seen.add(key)
                    job.update(country=country, mode=MODE_LABEL[mode], source="LinkedIn",
                               track="product" if TRACK_PRODUCT.search(job["title"]) else "uiux")
                    results.append(job)
                time.sleep(1.5)
    json.dump(results, sys.stdout, ensure_ascii=False, indent=1)
    print()


if __name__ == "__main__":
    main()
