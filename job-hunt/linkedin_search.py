"""Daily Job Hunt: LinkedIn public job search, last 3 days.

Prints a JSON list of design roles posted in the last 3 days: Product
Designer, UI/UX Designer, UX Designer and UI Designer, plain or Senior. Remote or hybrid
in Egypt; in the Gulf, only remote roles whose posting opens them to Egypt.
A plain-titled role is kept unless the posting asks for fewer than MIN_YEARS
years of experience (a range like "2-5 years" counts, since its top end is above it), so roles a senior designer can apply to stay in. Lead,
head, principal, staff, manager and junior roles are left out.

LinkedIn hides its workplace label (and ignores its remote/hybrid filter)
for signed-out visitors, so the work mode is read from each posting's own
text. Egypt postings whose text names no work mode are kept with mode
"Not stated" so they can be checked on LinkedIn; ones that say on-site only
are dropped.

Usage: python3 -B job-hunt/linkedin_search.py [--why]
  --why  also print every design posting checked, and why it was kept or skipped, to stderr
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
LAST_3_DAYS = "r259200"
MAX_AGE_DAYS = 3
PAGES = 3  # 10 results per page
MIN_YEARS = 3
WHY = "--why" in sys.argv

KEYWORDS = [
    "Product Designer",
    "UI UX Designer",
    "UX Designer",
    "UI Designer",
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

DESIGN = re.compile(
    r"(product designer|\bui\s*[/&-]?\s*ux\b|\bux\s*[/&-]?\s*ui\b|\bux designer\b|\bui designer\b|"
    r"user experience designer|user interface designer)", re.I)
SENIOR = re.compile(r"\b(senior|sr\.?)\b", re.I)
EXCLUDE = re.compile(
    r"\b(lead|leader|head|principal|staff|manager|director|chief|vp|founding|"
    r"junior|jr\.?|intern|internship|trainee|associate|entry|fresh|"
    r"graphic|motion|developer|engineer|researcher|research|writer|copywriter|"
    r"3d|interior|fashion|industrial|furniture|jewelry|packaging|architect)\b",
    re.I)
JUNIOR_LEVELS = {"Entry level", "Internship"}

ONSITE = re.compile(r"\b(on-?site|in-office|office-based|work(ing)? from (the |our )?office)\b", re.I)
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
YEARS = re.compile(r"(\d{1,2})\s*(?:\+|plus)?\s*(?:(?:-|–|to)\s*(\d{1,2})\s*)?\+?\s*(?:years|yrs)", re.I)


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
    """'Remote', 'Hybrid', 'On-site', or 'Not stated' when the posting doesn't say."""
    text = title + " . " + desc
    if FULLY_REMOTE.search(text):
        return "Remote"
    if HYBRID_TEXT.search(text):
        return "Hybrid"
    if REMOTE_TEXT.search(text):
        return "Remote"
    if ONSITE.search(text):
        return "On-site"
    return "Not stated"


def posting_details(job_id, title):
    """Description, work mode, years of experience asked for, and LinkedIn's seniority level."""
    page = get(POSTING + job_id)
    desc = field(r'show-more-less-html__markup[^>]*>(.*?)</div>', page)
    desc = html.unescape(re.sub(r"<[^>]+>", " ", desc))
    desc = re.sub(r"\s+", " ", desc).strip()
    years = [(int(m.group(1)), int(m.group(2) or m.group(1))) for m in YEARS.finditer(desc)
             if 0 < int(m.group(1)) <= 20]
    return {
        "description": desc[:1200],
        "mode": work_mode(title, desc),
        # The most demanding requirement, e.g. "5+" or "2-5".
        "yearsRequired": "-".join(map(str, sorted(set(max(years))))) if years else None,
        "seniorOk": None if not years else any(lo >= MIN_YEARS or hi > MIN_YEARS for lo, hi in years),
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


def rejection(job, d, country):
    """Why this posting is left out, or None when it qualifies."""
    if d["closed"]:
        return "closed"
    if d["seniorityLevel"] in JUNIOR_LEVELS:
        return "junior level"
    if d["mode"] == "On-site":
        return "on-site"
    # Egypt: Remote, Hybrid or Not stated all pass ("Not stated" is checked by hand on
    # LinkedIn). A Gulf role only counts if it can be done from Egypt: not hybrid, open
    # to Egypt (or MENA / EMEA / anywhere), and not asking the candidate to live there.
    if country != "Egypt":
        if d["mode"] == "Hybrid":
            return "hybrid in the Gulf"
        if d["needsGulfBase"]:
            return "must live in the Gulf or relocate"
        if not d["opensToEgypt"]:
            return "not open to Egypt"
    if not SENIOR.search(job["title"]) and d["seniorOk"] is False:
        return f"asks for only {d['yearsRequired']} years"
    return None


def main():
    seen, results = set(), []
    for loc, country in LOCATIONS:
        for kw in KEYWORDS:
            for p in range(PAGES):
                page = get(SEARCH + "?" + urllib.parse.urlencode(
                    {"keywords": kw, "location": loc, "f_TPR": LAST_3_DAYS, "start": p * 10}))
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
                    reason = rejection(job, details, country)
                    if WHY:
                        print(f"{'KEEP' if not reason else 'skip'} | {country} | {title} | {job['company']} | "
                              f"{reason or details['mode']} | {job['url']}", file=sys.stderr)
                    if reason:
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
