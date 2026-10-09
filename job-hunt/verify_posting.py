"""Daily Job Hunt: check a job posting found on Google (company careers page or ATS).

Reads the posting's structured data (schema.org JobPosting) and, for
Greenhouse, Lever and Ashby links, their public job APIs. Prints JSON with
the posting date, whether it is still open, the work mode and the countries
it is open to, so the daily routine can apply the same rules as LinkedIn.

Usage: python3 -B job-hunt/verify_posting.py <url> [<url> ...]
"""
import datetime
import html
import json
import re
import sys
import urllib.request

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0 Safari/537.36"
MAX_AGE_DAYS = 3

HYBRID = re.compile(r"\bhybrid\b", re.I)
REMOTE = re.compile(r"\b(remote|work from home|wfh|telecommut)", re.I)
ONSITE = re.compile(r"\b(on-?site|in-office|office-based)\b", re.I)
CLOSED = re.compile(r"(no longer (accepting|available|open)|position (has been )?(filled|closed)|job (is )?(closed|expired)|"
                    r"this job (post(ing)?|listing) (has )?(expired|closed))", re.I)


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "en-US,en;q=0.9"})
    try:
        with urllib.request.urlopen(req, timeout=25) as r:
            return r.status, r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, ""
    except Exception as e:  # network failure
        return None, str(e)


def to_date(value):
    """ISO date string, from an ISO timestamp or epoch milliseconds."""
    if value in (None, ""):
        return None
    if isinstance(value, (int, float)):
        return datetime.datetime.fromtimestamp(value / 1000, datetime.timezone.utc).date().isoformat()
    m = re.match(r"(\d{4}-\d{2}-\d{2})", str(value))
    return m.group(1) if m else None


def json_ld_postings(page):
    for block in re.findall(r'<script[^>]+application/ld\+json[^>]*>(.*?)</script>', page, re.S | re.I):
        try:
            data = json.loads(html.unescape(block.strip()))
        except ValueError:
            continue
        items = data if isinstance(data, list) else data.get("@graph", [data]) if isinstance(data, dict) else []
        for item in items:
            if isinstance(item, dict) and item.get("@type") in ("JobPosting", ["JobPosting"]):
                yield item


def countries(requirements):
    out = []
    for r in requirements if isinstance(requirements, list) else [requirements]:
        if isinstance(r, dict):
            out.append(r.get("name") or r.get("addressCountry") or "")
        elif r:
            out.append(str(r))
    return [c for c in out if c]


def from_json_ld(item):
    loc = item.get("jobLocation") or {}
    loc = loc[0] if isinstance(loc, list) and loc else loc
    addr = loc.get("address", {}) if isinstance(loc, dict) else {}
    return {
        "title": item.get("title"),
        "company": (item.get("hiringOrganization") or {}).get("name") if isinstance(item.get("hiringOrganization"), dict) else None,
        "postedDate": to_date(item.get("datePosted")),
        "validThrough": to_date(item.get("validThrough")),
        "remoteTag": item.get("jobLocationType") == "TELECOMMUTE",
        "openTo": countries(item.get("applicantLocationRequirements")),
        "location": ", ".join(x for x in [addr.get("addressLocality"), addr.get("addressCountry")] if isinstance(x, str) and x),
        "description": re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", item.get("description") or ""))).strip(),
    }


def from_ats_api(url):
    """Greenhouse, Lever and Ashby publish posting dates in their public job APIs."""
    m = re.search(r"greenhouse\.io/(?:embed/job_app\?for=)?([\w-]+)/jobs/(\d+)", url)
    if m:
        status, body = get(f"https://boards-api.greenhouse.io/v1/boards/{m.group(1)}/jobs/{m.group(2)}")
        if status == 200:
            d = json.loads(body)
            return {"title": d.get("title"), "postedDate": to_date(d.get("first_published") or d.get("updated_at")),
                    "location": (d.get("location") or {}).get("name", ""),
                    "description": re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", html.unescape(d.get("content") or ""))))}
        return {"closed": status == 404}
    m = re.search(r"jobs\.lever\.co/([\w.-]+)/([0-9a-f-]{36})", url)
    if m:
        status, body = get(f"https://api.lever.co/v0/postings/{m.group(1)}/{m.group(2)}")
        if status == 200:
            d = json.loads(body)
            cats = d.get("categories") or {}
            return {"title": d.get("text"), "postedDate": to_date(d.get("createdAt")),
                    "location": ", ".join(cats.get("allLocations") or [cats.get("location") or ""]),
                    "remoteTag": d.get("workplaceType") == "remote", "workplaceType": d.get("workplaceType"),
                    "description": d.get("descriptionPlain") or ""}
        return {"closed": status == 404}
    m = re.search(r"jobs\.ashbyhq\.com/([\w.-]+)/([0-9a-f-]{36})", url)
    if m:
        status, body = get(f"https://api.ashbyhq.com/posting-api/job-board/{m.group(1)}")
        if status == 200:
            for d in json.loads(body).get("jobs", []):
                if m.group(2) in (d.get("id"), d.get("jobUrl", "")) or m.group(2) in d.get("jobUrl", ""):
                    return {"title": d.get("title"), "postedDate": to_date(d.get("publishedAt")),
                            "location": d.get("location", ""), "remoteTag": bool(d.get("isRemote")),
                            "workplaceType": d.get("workplaceType"), "description": d.get("descriptionPlain") or ""}
            return {"closed": True}
    return {}


def verify(url):
    status, page = get(url)
    info = {"url": url, "httpStatus": status}
    if status == 200:
        items = list(json_ld_postings(page))
        if items:
            info.update({k: v for k, v in from_json_ld(items[0]).items() if v not in (None, "", [])})
        info["closed"] = bool(CLOSED.search(page))
    elif status in (403, 429, 503):
        info["blocked"] = True  # bot protection or rate limit: can't confirm anything
    elif status in (404, 410):
        info["closed"] = True
    for k, v in from_ats_api(url).items():
        if v not in (None, "", []) and not info.get(k):
            info[k] = v

    text = f"{info.get('title', '')} . {info.get('location', '')} . {info.get('description', '')}"
    wt = (info.get("workplaceType") or "").lower()
    if wt in ("remote", "hybrid", "onsite", "on-site"):
        info["mode"] = {"onsite": "On-site", "on-site": "On-site"}.get(wt, wt.capitalize())
    elif HYBRID.search(text):
        info["mode"] = "Hybrid"
    elif info.get("remoteTag") or REMOTE.search(text):
        info["mode"] = "Remote"
    elif ONSITE.search(text):
        info["mode"] = "On-site"
    else:
        info["mode"] = "Not stated"

    today = datetime.date.today()
    posted = info.get("postedDate")
    info["ageDays"] = (today - datetime.date.fromisoformat(posted)).days if posted else None
    info["recent"] = info["ageDays"] is not None and info["ageDays"] <= MAX_AGE_DAYS
    if info.get("validThrough") and info["validThrough"] < today.isoformat():
        info["closed"] = True
    info["description"] = (info.get("description") or "")[:800]
    return info


if __name__ == "__main__":
    json.dump([verify(u) for u in sys.argv[1:]], sys.stdout, ensure_ascii=False, indent=1)
    print()
