"""Daily Job Hunt: LinkedIn public job search, last 48 hours.

Prints a JSON list of product / UI-UX design roles posted in the last 48
hours: Product Designer and UI/UX Designer, plain or Senior. Remote or hybrid
in Egypt, remote in the Gulf. A plain-titled role is kept unless the posting
asks for fewer than MIN_YEARS years of experience, so roles a senior designer
can apply to stay in. Lead, head, principal, staff, manager and junior roles
are left out.

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
POSTING = "https://www.linkedin.com/jobs-guest/jobs/api/jobPosting/"
LAST_48H = "r172800"
REMOTE, HYBRID = "2", "3"
PAGES = 3  # 10 results per page
MIN_YEARS = 3

KEYWORDS = [
    "Product Designer",
    "UI UX Designer",
]
# (LinkedIn location, country label, allowed work modes)
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

DESIGN = re.compile(r"(product designer|\bui\s*[/&-]?\s*ux\b|\bux\s*[/&-]?\s*ui\b)", re.I)
SENIOR = re.compile(r"\b(senior|sr\.?)\b", re.I)
EXCLUDE = re.compile(
    r"\b(lead|leader|head|principal|staff|manager|director|chief|vp|founding|"
    r"junior|jr\.?|intern|internship|trainee|associate|entry|fresh|"
    r"graphic|motion|developer|engineer|researcher|research|writer|copywriter|"
    r"3d|interior|fashion|industrial|furniture|jewelry|packaging|architect)\b",
    re.I)
ONSITE = re.compile(r"\b(on-?site|in-office|office-based|work from (the )?office)\b", re.I)
REMOTE_OR_HYBRID = re.compile(r"\b(remote|hybrid|work from home|wfh)\b", re.I)
JUNIOR_LEVELS = {"Entry level", "Internship"}
YEARS = re.compile(r"(\d{1,2})\s*(?:\+|plus)?\s*(?:[-–to]+\s*\d{1,2}\s*)?\+?\s*(?:years|yrs)", re.I)


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0", "Accept-Language": "en-US,en;q=0.9"})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=25) as r:
                return r.read().decode("utf-8", "replace")
        except Exception as e:  # 429 / transient network errors
            print(f"warn: {url[:110]}: {e}", file=sys.stderr)
            time.sleep(10 * (attempt + 1))
    return ""


def field(pattern, text):
    m = re.search(pattern, text, re.S)
    return html.unescape(m.group(1)).strip() if m else ""


def parse_cards(page):
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


def posting_details(job_id):
    """Description text, years of experience asked for, and LinkedIn's seniority level."""
    page = get(POSTING + job_id)
    desc = field(r'show-more-less-html__markup[^>]*>(.*?)</div>', page)
    desc = html.unescape(re.sub(r"<[^>]+>", " ", desc))
    desc = re.sub(r"\s+", " ", desc).strip()
    years = [int(m.group(1)) for m in YEARS.finditer(desc) if 0 < int(m.group(1)) <= 20]
    level = field(r'Seniority level\s*</h3>\s*<span[^>]*>\s*(.*?)\s*<', page)
    closed = "No longer accepting applications" in page
    # LinkedIn's remote/hybrid filter is sometimes wrong: trust a description that says on-site only.
    onsite = bool(ONSITE.search(desc)) and not REMOTE_OR_HYBRID.search(desc)
    return {"description": desc[:1200], "yearsRequired": max(years) if years else None,
            "seniorityLevel": level, "closed": closed, "onsite": onsite}


def main():
    seen, results = set(), []
    for loc, country, modes in LOCATIONS:
        for mode in modes:
            for kw in KEYWORDS:
                for p in range(PAGES):
                    page = get(SEARCH + "?" + urllib.parse.urlencode(
                        {"keywords": kw, "location": loc, "f_TPR": LAST_48H, "f_WT": mode, "start": p * 10}))
                    cards = list(parse_cards(page))
                    for job in cards:
                        m = re.search(r"-(\d+)$", job["url"])
                        if not m or m.group(1) in seen:
                            continue
                        seen.add(m.group(1))
                        title = job["title"]
                        if not DESIGN.search(title) or EXCLUDE.search(title):
                            continue
                        details = posting_details(m.group(1))
                        time.sleep(1.5)
                        if details["closed"] or details["onsite"] or details["seniorityLevel"] in JUNIOR_LEVELS:
                            continue
                        senior_title = bool(SENIOR.search(title))
                        years = details["yearsRequired"]
                        if not senior_title and years is not None and years < MIN_YEARS:
                            continue
                        job.update(details, country=country, mode=MODE_LABEL[mode], source="LinkedIn",
                                   seniorTitle=senior_title,
                                   track="product" if re.search(r"product design", title, re.I) else "uiux")
                        results.append(job)
                    time.sleep(2.5)
                    if len(cards) < 10:
                        break
    json.dump(results, sys.stdout, ensure_ascii=False, indent=1)
    print()


if __name__ == "__main__":
    main()
