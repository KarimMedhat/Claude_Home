"""Daily Job Hunt: check LinkedIn feed posts (HR "we're hiring" posts) found on Google.

A post's URL carries its activity id, and the id's top bits are the time it
was posted, so the date is exact without trusting a search snippet. The
public post page is then read for its text, to see whether it is a design
hiring post and where the role is.

Usage: python3 -B job-hunt/linkedin_posts.py <post url> [<post url> ...]
"""
import datetime
import html
import json
import re
import sys
import urllib.request

MAX_AGE_DAYS = 3
HIRING = re.compile(r"\b(hiring|we're looking|we are looking|join our team|open (role|position)|vacanc|job opening|"
                    r"send (your )?(cv|resume)|apply)\b", re.I)
DESIGN = re.compile(r"(product designer|\bui\s*[/&-]?\s*ux\b|\bux\s*[/&-]?\s*ui\b|\bux designer\b|\bui designer\b)", re.I)
TOO_SENIOR_OR_JUNIOR = re.compile(r"\b(lead|head of|principal|staff|design manager|intern|internship|junior|fresh grad)", re.I)
PLACES = {
    "Egypt": re.compile(r"\b(egypt|cairo|giza|alexandria|new cairo|maadi|smart village)\b", re.I),
    "Gulf": re.compile(r"\b(saudi|ksa|riyadh|jeddah|uae|dubai|abu dhabi|qatar|doha|kuwait|bahrain|oman)\b", re.I),
}
REMOTE = re.compile(r"\b(remote|work from home|wfh)\b", re.I)
HYBRID = re.compile(r"\bhybrid\b", re.I)
ONSITE = re.compile(r"\b(on-?site|onsite|from (the|our) office)\b", re.I)
# Patterns common in recruitment-funnel and scam posts: no employer named, apply by joining a group or chat.
RED_FLAGS = {
    "apply by joining a group": re.compile(r"\b(must be a member|join (our|the) .{0,40}(room|group|community|channel)|join through the following link)", re.I),
    "apply over Telegram/WhatsApp": re.compile(r"\b(telegram|whatsapp|t\.me/|wa\.me/)", re.I),
    "asks for a fee": re.compile(r"\b(registration fee|application fee|training fee|pay (a|the) fee)\b", re.I),
}


def posted_at(url):
    m = re.search(r"(?:activity|share|ugcPost)[-:](\d{18,20})", url)
    if not m:
        return None
    return datetime.datetime.fromtimestamp((int(m.group(1)) >> 22) / 1000, datetime.timezone.utc)


def read_post(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0", "Accept-Language": "en-US,en;q=0.9"})
    try:
        with urllib.request.urlopen(req, timeout=25) as r:
            page = r.read().decode("utf-8", "replace")
    except Exception as e:
        return {"error": str(e)}
    body = ""
    for block in re.findall(r'<script[^>]+application/ld\+json[^>]*>(.*?)</script>', page, re.S):
        try:
            data = json.loads(block)
        except ValueError:
            continue
        if isinstance(data, dict) and data.get("articleBody"):
            author = data.get("author") or {}
            return {"text": data["articleBody"], "author": author.get("name") if isinstance(author, dict) else None}
    m = re.search(r'<meta property="og:description" content="([^"]*)"', page)
    if m:
        body = html.unescape(m.group(1))
    return {"text": body, "author": None}


def check(url):
    when = posted_at(url)
    info = {"url": url, "postedDate": when.date().isoformat() if when else None}
    info["ageDays"] = (datetime.datetime.now(datetime.timezone.utc) - when).days if when else None
    info["recent"] = info["ageDays"] is not None and info["ageDays"] <= MAX_AGE_DAYS
    if not info["recent"]:
        return info  # no need to open old posts
    post = read_post(url)
    text = post.get("text") or ""
    info.update(author=post.get("author"), text=text[:1500], error=post.get("error"))
    info["isDesignHiring"] = bool(HIRING.search(text) and DESIGN.search(text))
    info["tooSeniorOrJunior"] = bool(TOO_SENIOR_OR_JUNIOR.search(text))
    info["places"] = [name for name, rx in PLACES.items() if rx.search(text)]
    info["mode"] = ("Hybrid" if HYBRID.search(text) else "Remote" if REMOTE.search(text)
                    else "On-site" if ONSITE.search(text) else "Not stated")
    info["redFlags"] = [name for name, rx in RED_FLAGS.items() if rx.search(text)]
    return info


if __name__ == "__main__":
    json.dump([check(u) for u in sys.argv[1:]], sys.stdout, ensure_ascii=False, indent=1)
    print()
