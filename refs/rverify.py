#!/usr/bin/env python3
"""Verify refs/refs.csv: every URL answers HTTP 200 and its <title>/<h1> loosely
matches the stated title. Results are cached in .cache/refs.json.

  python3 refs/rverify.py          check all rows, exit 1 listing bad ones
  python3 refs/rverify.py --fix    fill empty titles (and replace mismatched ones)
                                   from the page, then re-check
  python3 refs/rverify.py --refresh  ignore the cache
"""
import csv, html, json, re, sys, time, urllib.request, urllib.error
from pathlib import Path

HERE = Path(__file__).resolve().parent
CSV = HERE / "refs.csv"
CACHE = HERE.parent / ".cache" / "refs.json"
HEADER = ["topic", "site", "url", "title"]
SITES = {"cp-algorithms", "usaco-guide", "visualgo", "other"}
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120.0 Safari/537.36")
DELAY = 0.6


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "text/html,*/*"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            body = r.read(400000).decode("utf-8", "replace")
            return r.status, body
    except urllib.error.HTTPError as e:
        return e.code, ""
    except Exception as e:  # network error
        return 0, str(e)


def clean(s):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", s))).strip()


SUFFIX = re.compile(r"\s*(?:[-\u00b7|\u2013]\s*(?:Algorithms for Competitive Programming|USACO Guide|VisuAlgo|RFC Editor))\s*$", re.I)


def page_info(body):
    t = re.search(r"<title[^>]*>(.*?)</title>", body, re.S | re.I)
    h = re.search(r"<h1[^>]*>(.*?)</h1>", body, re.S | re.I)
    title = SUFFIX.sub("", clean(t.group(1))) if t else ""
    title = re.sub(r"^\[\d{4}\.\d{4,5}\]\s*", "", title)
    title = re.sub(r"^PostgreSQL: Documentation: \d+: ", "PostgreSQL: ", title)
    return title, (clean(h.group(1)).rstrip("\u00b6 ") if h else "")


def norm(s):
    s = s.lower().replace("’", "'")
    return re.sub(r"[^a-z0-9]+", " ", s).strip()


def matches(stated, title, h1):
    a = norm(stated)
    if not a:
        return False
    for page in (norm(title), norm(h1)):
        if a in page or (page and page in a):
            return True
    words = set(a.split())
    pw = set(norm(title).split()) | set(norm(h1).split())
    return len(words & pw) >= max(1, 0.6 * len(words))


def load_cache():
    try:
        return json.loads(CACHE.read_text())
    except Exception:
        return {}


def main():
    fix = "--fix" in sys.argv
    refresh = "--refresh" in sys.argv
    rows = list(csv.DictReader(open(CSV, newline="")))
    cache = {} if refresh else load_cache()
    bad, last = [], 0
    seen = set()
    for i, r in enumerate(rows, start=2):
        url = r["url"]
        if r["site"] not in SITES:
            bad.append(f"line {i} {r['topic']}: bad site {r['site']!r}")
        if (r["topic"], url) in seen:
            bad.append(f"line {i} {r['topic']}: duplicate row")
        seen.add((r["topic"], url))
        if url not in cache or cache[url].get("status") != 200:
            wait = DELAY - (time.time() - last)
            if wait > 0:
                time.sleep(wait)
            st, body = fetch(url)
            last = time.time()
            t, h = page_info(body) if st == 200 else ("", "")
            cache[url] = {"status": st, "title": t, "h1": h, "time": int(time.time())}
            CACHE.parent.mkdir(exist_ok=True)
            CACHE.write_text(json.dumps(cache, indent=1))
        c = cache[url]
        if c["status"] != 200:
            bad.append(f"line {i} {r['topic']} {url}: HTTP {c['status']}")
            continue
        if fix and (not r["title"] or not matches(r["title"], c["title"], c["h1"])):
            r["title"] = c["title"] or c["h1"]
        if not matches(r["title"], c["title"], c["h1"]):
            bad.append(f"line {i} {r['topic']} {url}: title {r['title']!r} vs page {c['title']!r} / {c['h1']!r}")
    if fix:
        with open(CSV, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=HEADER)
            w.writeheader()
            w.writerows(rows)
    per = {}
    for r in rows:
        per[r["topic"]] = per.get(r["topic"], 0) + 1
    for t, n in per.items():
        if n > 3:
            bad.append(f"{t}: {n} refs (max 3)")
    print(f"{len(rows)} rows, {len(per)} topics, {len(bad)} bad")
    for b in bad:
        print("BAD", b)
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
