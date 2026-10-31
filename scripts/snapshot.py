#!/usr/bin/env python3
"""Daily VulnWatch snapshot: CISA KEV + FIRST EPSS, plus a short digest.

Each step writes its own files and, with --commit, makes its own commit, so the
git history reads as a day-by-day changelog of what was exploited.

  python scripts/snapshot.py            # fetch and write files only
  python scripts/snapshot.py --commit   # also commit after each step

Standard library only. If `certifi` is installed it is used for SSL, which helps
on python.org builds of Python for macOS.
"""
import argparse
import csv
import datetime as dt
import json
import ssl
import subprocess
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
DIGESTS = ROOT / "digests"
README = ROOT / "README.md"

KEV_URL = "https://raw.githubusercontent.com/cisagov/kev-data/develop/known_exploited_vulnerabilities.json"
EPSS_URL = "https://api.first.org/data/v1/epss"
USER_AGENT = "VulnWatch-UK daily snapshot (+https://github.com/SMCallan/VulnWatch-UK)"

README_START, README_END = "<!-- digest:start -->", "<!-- digest:end -->"
TODAY = dt.datetime.now(dt.timezone.utc).date().isoformat()

try:
    import certifi

    SSL_CTX = ssl.create_default_context(cafile=certifi.where())
except ImportError:
    SSL_CTX = None


# ---------------------------------------------------------------- helpers

def get_json(url, tries=4):
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"})
    for attempt in range(1, tries + 1):
        try:
            with urllib.request.urlopen(req, timeout=60, context=SSL_CTX) as resp:
                return json.load(resp)
        except (urllib.error.URLError, TimeoutError):
            if attempt == tries:
                raise
            time.sleep(2 ** attempt)


def load_json(path, default=None):
    try:
        return json.loads(path.read_text())
    except (FileNotFoundError, ValueError):
        return default


def commit(paths, message, enabled):
    if not enabled:
        print(f"  wrote   {message}")
        return
    subprocess.run(["git", "add", "--", *map(str, paths)], cwd=ROOT, check=True)
    if subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=ROOT).returncode == 0:
        print(f"  skip    {message} (no changes)")
        return
    subprocess.run(["git", "commit", "-q", "-m", message], cwd=ROOT, check=True)
    print(f"  commit  {message}")


def cve_link(cve):
    return f"[{cve}](https://nvd.nist.gov/vuln/detail/{cve})"


def cell(text):
    return str(text or "").replace("|", "\\|").replace("\n", " ").strip()


def pct(x):
    return f"{x * 100:.1f}%"


# ---------------------------------------------------------------- steps

def previous_run_date():
    """Date of the last run before today, from history.csv (None on the first run)."""
    path = DATA / "history.csv"
    if not path.exists():
        return None
    with path.open(newline="") as f:
        return max((r["date"] for r in csv.DictReader(f) if r.get("date", "") < TODAY), default=None)


def fetch_kev(since):
    """Return the catalogue and the entries added on or after `since`.

    Going by dateAdded rather than diffing against the last snapshot keeps the
    answer the same if the workflow is re-run later the same day. CISA publishes
    in US hours, well after the 06:17 UTC run, so entries dated on the previous
    run's day were not in that run.
    """
    kev = get_json(KEV_URL)
    vulns = kev.get("vulnerabilities", [])
    new = [v for v in vulns if v.get("dateAdded", "") >= since]
    new.sort(key=lambda v: v.get("dateAdded", ""), reverse=True)
    return kev, new


def fetch_epss(cves, prev):
    """EPSS scores for the given CVEs as [epss, percentile, change since the previous model run]."""
    scores, model_date = {}, None
    for i in range(0, len(cves), 100):
        query = urllib.parse.urlencode({"cve": ",".join(cves[i:i + 100]), "limit": 100})
        for row in get_json(f"{EPSS_URL}?{query}").get("data", []):
            scores[row["cve"]] = [round(float(row["epss"]), 5), round(float(row["percentile"]), 5)]
            model_date = row.get("date", model_date)
        time.sleep(0.3)

    prev_model = (prev.get("meta") or {}).get("model_date")
    prev_scores = prev.get("scores", {})
    for cve, s in scores.items():
        old = prev_scores.get(cve)
        if not old:
            change = None
        elif model_date != prev_model:
            change = round(s[0] - old[0], 5)
        else:
            # Same model as last time (a re-run): keep the change we already worked out.
            change = old[2] if len(old) > 2 else None
        s.append(change)
    return scores, model_date


def cve_sort_key(cve):
    _, year, num = cve.split("-")
    return int(year), int(num)


def fetch_top_epss(limit=100, threshold=0.9):
    # The API ignores `order`, so pull everything above the threshold and sort here.
    rows, offset = [], 0
    while True:
        page = get_json(f"{EPSS_URL}?epss-gt={threshold}&limit=1000&offset={offset}")
        rows += page.get("data", [])
        offset += 1000
        if offset >= int(page.get("total", 0)):
            break
    top = [
        {"cve": r["cve"], "epss": round(float(r["epss"]), 5), "percentile": round(float(r["percentile"]), 5)}
        for r in rows
    ]
    # Highest score first; ties go to the most recent CVE.
    top.sort(key=lambda r: (r["epss"], cve_sort_key(r["cve"])), reverse=True)
    return top[:limit]


def write_scores(path, meta, scores):
    # One CVE per line keeps the daily diffs readable.
    lines = [f'    "{cve}": {json.dumps(v)}' for cve, v in sorted(scores.items())]
    path.write_text(
        "{\n"
        f'  "meta": {json.dumps(meta)},\n'
        '  "scores": {\n' + ",\n".join(lines) + "\n  }\n}\n"
    )


def build_digest(kev, new, scores, top, model_date, first_run):
    """Return (full digest markdown, short summary for the README)."""
    vulns = kev.get("vulnerabilities", [])
    by_id = {v["cveID"]: v for v in vulns}
    ransomware = sum(1 for v in vulns if v.get("knownRansomwareCampaignUse") == "Known")
    new_label = "Added in the last 7 days" if first_run else "New since last snapshot"

    def who(cve):
        v = by_id.get(cve, {})
        return cell(f"{v.get('vendorProject', '')} {v.get('product', '')}")

    headline = [
        f"- **KEV catalogue:** {len(vulns):,} known exploited vulnerabilities (version {kev.get('catalogVersion', '?')})",
        f"- **{new_label}:** {len(new)}",
        f"- **Known ransomware use:** {ransomware:,}",
        f"- **EPSS model date:** {model_date or 'n/a'}",
    ]

    new_table = []
    if new:
        new_table = [
            "| CVE | Vendor / product | Vulnerability | Added | Due | Ransomware | EPSS |",
            "|---|---|---|---|---|---|---|",
        ]
        for v in new:
            e = scores.get(v["cveID"])
            new_table.append(
                f"| {cve_link(v['cveID'])} | {who(v['cveID'])} | {cell(v.get('vulnerabilityName'))} "
                f"| {v.get('dateAdded', '')} | {v.get('dueDate', '')} "
                f"| {cell(v.get('knownRansomwareCampaignUse'))} | {pct(e[0]) if e else 'n/a'} |"
            )

    # The all-time top is always the same 2014-2020 classics, so stick to the last year.
    year_ago = (dt.date.fromisoformat(TODAY) - dt.timedelta(days=365)).isoformat()
    recent = [(c, s) for c, s in scores.items() if by_id.get(c, {}).get("dateAdded", "") >= year_ago]
    top_kev = sorted(recent, key=lambda kv: kv[1][0], reverse=True)[:10]
    top_kev_table = ["| CVE | Vendor / product | Added | EPSS | Percentile |", "|---|---|---|---|---|"] + [
        f"| {cve_link(c)} | {who(c)} | {by_id[c].get('dateAdded', '')} | {pct(s[0])} | {pct(s[1])} |"
        for c, s in top_kev
    ]

    risers = sorted(
        ((c, s[0], s[2]) for c, s in scores.items() if s[2] and s[2] > 0),
        key=lambda r: r[2],
        reverse=True,
    )[:10]
    risers_table = []
    if risers:
        risers_table = ["| CVE | Vendor / product | EPSS | Change |", "|---|---|---|---|"] + [
            f"| {cve_link(c)} | {who(c)} | {pct(e)} | +{d * 100:.1f} pts |" for c, e, d in risers
        ]

    not_in_kev = [r for r in top if r["cve"] not in by_id][:10]
    watch_table = ["| CVE | EPSS | Percentile |", "|---|---|---|"] + [
        f"| {cve_link(r['cve'])} | {pct(r['epss'])} | {pct(r['percentile'])} |" for r in not_in_kev
    ]

    sources = (
        "Sources: [CISA KEV](https://www.cisa.gov/known-exploited-vulnerabilities-catalog) · "
        "[FIRST EPSS](https://www.first.org/epss/)"
    )

    full = [f"# VulnWatch daily digest: {TODAY}", "", *headline, ""]
    if new_table:
        full += [f"## {new_label}", "", *new_table, ""]
    full += ["## Most likely to be exploited (added to KEV in the last year)", "", *top_kev_table, ""]
    if risers_table:
        full += ["## Biggest EPSS rises since the previous model run", "", *risers_table, ""]
    full += [
        "## High EPSS, not yet in KEV",
        "",
        "CVEs with the highest predicted exploitation that CISA hasn't added to KEV yet. Worth watching.",
        "",
        *watch_table,
        "",
        sources,
        "",
    ]

    summary = [f"**{TODAY}**", "", *headline, ""]
    if new_table:
        shown = new_table[:2 + 5]
        summary += [f"**{new_label}**", "", *shown]
        if len(new) > 5:
            summary.append(f"| … and {len(new) - 5} more | | | | | | |")
        summary.append("")
    summary.append(f"[Full digest →](digests/{TODAY}.md) · [All digests](digests/)")

    return "\n".join(full), "\n".join(summary)


def update_history(row):
    path = DATA / "history.csv"
    rows = []
    if path.exists():
        with path.open(newline="") as f:
            rows = [r for r in csv.DictReader(f) if r.get("date") != row["date"]]
    rows.append(row)
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(row))
        writer.writeheader()
        writer.writerows(rows)


def update_readme(summary):
    text = README.read_text() if README.exists() else ""
    block = f"{README_START}\n{summary}\n{README_END}"
    if README_START in text and README_END in text:
        start, end = text.index(README_START), text.index(README_END) + len(README_END)
        text = text[:start] + block + text[end:]
    else:
        text = text.rstrip() + "\n\n" + block + "\n"
    README.write_text(text)


# ---------------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--commit", action="store_true", help="commit after each step")
    args = ap.parse_args()

    DATA.mkdir(exist_ok=True)
    DIGESTS.mkdir(exist_ok=True)
    prev_date = previous_run_date()
    first_run = prev_date is None
    # First run: nothing to compare against, so show the last week instead.
    since = prev_date or (dt.date.fromisoformat(TODAY) - dt.timedelta(days=7)).isoformat()
    print(f"VulnWatch snapshot for {TODAY} (new since {since})")

    # 1. KEV catalogue
    kev, new = fetch_kev(since)
    vulns = kev.get("vulnerabilities", [])
    (DATA / "kev.json").write_text(json.dumps(kev, indent=2, ensure_ascii=False) + "\n")
    msg = (
        f"KEV: initial snapshot, {len(vulns):,} entries"
        if first_run
        else f"KEV: {len(new)} new, {len(vulns):,} total (catalogue {kev.get('catalogVersion', '?')})"
    )
    commit([DATA / "kev.json"], msg, args.commit)

    # 2. EPSS scores for every KEV CVE
    scores, model_date = fetch_epss(sorted(v["cveID"] for v in vulns), load_json(DATA / "epss-kev.json") or {})
    write_scores(DATA / "epss-kev.json", {"model_date": model_date, "count": len(scores)}, scores)
    commit([DATA / "epss-kev.json"], f"EPSS: scores for {len(scores):,} KEV CVEs (model {model_date})", args.commit)

    # 3. Top 100 CVEs overall by EPSS
    top = fetch_top_epss()
    (DATA / "epss-top100.json").write_text(
        json.dumps({"model_date": model_date, "cves": top}, indent=1) + "\n"
    )
    commit([DATA / "epss-top100.json"], f"EPSS: top 100 CVEs by exploitation likelihood ({model_date})", args.commit)

    # 4. Daily digest
    full, summary = build_digest(kev, new, scores, top, model_date, first_run)
    digest_path = DIGESTS / f"{TODAY}.md"
    digest_path.write_text(full)
    commit([digest_path], f"Digest: {TODAY} ({len(new)} new KEV entries)", args.commit)

    # 5. Metrics history
    epss_values = [s[0] for s in scores.values()]
    top_cve = max(scores.items(), key=lambda kv: kv[1][0])[0] if scores else ""
    update_history({
        "date": TODAY,
        "kev_total": len(vulns),
        "kev_new": len(new),
        "kev_ransomware": sum(1 for v in vulns if v.get("knownRansomwareCampaignUse") == "Known"),
        "kev_mean_epss": round(sum(epss_values) / len(epss_values), 4) if epss_values else "",
        "kev_epss_over_50pct": sum(1 for e in epss_values if e >= 0.5),
        "kev_top_epss_cve": top_cve,
    })
    commit([DATA / "history.csv"], f"History: add metrics for {TODAY}", args.commit)

    # 6. README summary
    update_readme(summary)
    commit([README], f"README: today's summary ({TODAY})", args.commit)


if __name__ == "__main__":
    main()
