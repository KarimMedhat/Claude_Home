"""Daily Job Hunt: LinkedIn public job search, last 48 hours.

Prints a JSON list of product / UI-UX design roles posted in the last 48
hours: Product Designer and UI/UX Designer, plain or Senior. Remote or hybrid
in Egypt; in the Gulf, only remote roles whose posting opens them to Egypt.
A plain-titled role is kept unless the posting asks for fewer than MIN_YEARS
years of experience, so roles a senior designer can apply to stay in. Lead,
head, principal, staff, manager and junior roles are left out.

LinkedIn's public search ignores its remote/hybrid filter, so the work mode
is read from each posting's own text; a posting that names neither is
skipped.

Usage: python3 -B job-hunt/linkedin_search.py
"""
import datetime
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
MAX_AGE_DAYS = 2
PAGES = 3  # 10 results per page
MIN_YEARS = 3

KEYWORDS = [
    "Product Designer",
    "UI UX Designer",
]
# (LinkedIn location, country label)
LOCATIONS = [
    ("Egypt", "Egypt"),
    ("Saudi Arabia", "Saudi Arabia"),
    ("United Arab Emirates", "UAE"),
    ("Qatar", "Qatar"),
    ("Kuwait", "Kuwait"),
    ("Bahrain", "Bahrain"),
    ("Oman", "Oman"),
]

DESIGN = re.compile(r"(product designer|\bui\s*[/&-]?\s*ux\b|\bux\s*[/&-]?\s*ui\b)", re.I)
SENIOR = re.compile(r"\b(senior|sr\.?)\b", re.I)
EXCLUDE = re.compile(
    r"\b(lead|leader|head|principal|staff|manager|director|chief|vp|founding|"
    r"junior|jr\.?|intern|internship|trainee|associate|entry|fresh|"
    r"graphic|motion|developer|engineer|researcher|research|writer|copywriter|"
    r"3d|interior|fashion|industrial|furniture|jewelry|packaging|architect)\b",
    re.I)
JUNIOR_LEVELS = {"Entry level", "Internship"}

FULLY_REMOTE = re.compile(r"\b(fully remote|100% remote|remote only|remote-only)\b", re.I)
HYBRID_TEXT = re.compile(r"\bhybrid\b", re.I)
REMOTE_TEXT = re.compile(
    r"(\bremote[- ](role|position|job|opportunity|work|working|first|friendly|based|setup|contract)\b|"
    r"\b(work|working) (from home|remotely)\b|\bwfh\b|"
    r"\b(location|workplace|work mode|work type|work model)\s*[:\-]\s*remote\b|"
    r"\bthis (is a|role is|position is|job is) (fully )?remote\b|\(remote\)|\bremote\s*[,|/)]|[-–]\s*remote\b)",
    re.I)

GULF = r"(the )?(gcc|gulf|uae|united arab emirates|dubai|abu dhabi|sharjah|saudi( arabia)?|ksa|riyadh|jeddah|qatar|doha|kuwait|bahrain|manama|oman|muscat)"
OPEN_TO_EGYPT = re.compile(
    r"\b(egypt|cairo|mena|middle east and north africa|emea|anywhere|worldwide|any country|any location|"
    r"all countries|globally|fully distributed)\b", re.I)
GULF_BASE = re.compile(
    r"relocat|\b(based|located|reside|resident|residing|living)\s+(in|within)\s+" + GULF + r"\b", re.I)
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


def work_mode(title, desc):
    """'Remote', 'Hybrid', or None when the posting doesn't say."""
    text = title + " . " + desc
    if FULLY_REMOTE.search(text):
        return "Remote"
    if HYBRID_TEXT.search(text):
        return "Hybrid"
    if REMOTE_TEXT.search(text):
        return "Remote"
    return None


def posting_details(job_id, title):
    """Description, work mode, years of experience asked for, and LinkedIn's seniority level."""
    page = get(POSTING + job_id)
    desc = field(r'show-more-less-html__markup[^>]*>(.*?)</div>', page)
    desc = html.unescape(re.sub(r"<[^>]+>", " ", desc))
    desc = re.sub(r"\s+", " ", desc).strip()
    years = [int(m.group(1)) for m in YEARS.finditer(desc) if 0 < int(m.group(1)) <= 20]
    return {
        "description": desc[:1200],
        "mode": work_mode(title, desc),
        "yearsRequired": max(years) if years else None,
        "seniorityLevel": field(r'Seniority level\s*</h3>\s*<span[^>]*>\s*(.*?)\s*<', page),
        "closed": "No longer accepting applications" in page,
        "needsGulfBase": bool(GULF_BASE.search(desc)),
        "opensToEgypt": bool(OPEN_TO_EGYPT.search(desc)),
    }


def recent(posted_date):
    try:
        d = datetime.date.fromisoformat(posted_date)
    except ValueError:
        return False
    return (datetime.date.today() - d).days <= MAX_AGE_DAYS


def qualifies(job, d, country):
    if d["closed"] or d["seniorityLevel"] in JUNIOR_LEVELS:
        return False
    if country == "Egypt":
        if d["mode"] not in ("Remote", "Hybrid"):
            return False
    # A Gulf role only counts if it can be done from Egypt: remote, open to Egypt
    # (or MENA / EMEA / anywhere), and not asking the candidate to live in the Gulf.
    elif d["mode"] != "Remote" or d["needsGulfBase"] or not d["opensToEgypt"]:
        return False
    years = d["yearsRequired"]
    return bool(SENIOR.search(job["title"])) or years is None or years >= MIN_YEARS


def main():
    seen, results = set(), []
    for loc, country in LOCATIONS:
        for kw in KEYWORDS:
            for p in range(PAGES):
                page = get(SEARCH + "?" + urllib.parse.urlencode(
                    {"keywords": kw, "location": loc, "f_TPR": LAST_48H, "start": p * 10}))
                cards = list(parse_cards(page))
                for job in cards:
                    m = re.search(r"-(\d+)$", job["url"])
                    if not m or m.group(1) in seen:
                        continue
                    seen.add(m.group(1))
                    title = job["title"]
                    if not DESIGN.search(title) or EXCLUDE.search(title) or not recent(job["postedDate"]):
                        continue
                    details = posting_details(m.group(1), title)
                    time.sleep(1.5)
                    if not qualifies(job, details, country):
                        continue
                    job.update(details, country=country, source="LinkedIn",
                               seniorTitle=bool(SENIOR.search(title)),
                               track="product" if re.search(r"product design", title, re.I) else "uiux")
                    results.append(job)
                time.sleep(2.5)
                if len(cards) < 10:
                    break
    json.dump(results, sys.stdout, ensure_ascii=False, indent=1)
    print()


if __name__ == "__main__":
    main()
