# VulnWatch UK

Vulnerability-intelligence portal that combines CISA's **Known Exploited Vulnerabilities** (KEV) catalogue with FIRST's **EPSS** exploit-likelihood scores, with quick links to NVD, CVE.org, Exploit-DB, AttackerKB and OSV.

**Live site:** https://smcallan.github.io/VulnWatch-UK/

## Daily snapshot

A [GitHub Actions workflow](.github/workflows/daily-snapshot.yml) runs every morning at 06:17 UTC. Each step is its own commit, so the git history doubles as a day-by-day log of what's being exploited:

1. **KEV:** snapshots the full catalogue to [`data/kev.json`](data/kev.json) and notes what's new
2. **EPSS:** fetches scores for every KEV CVE to [`data/epss-kev.json`](data/epss-kev.json)
3. **Top 100:** saves the 100 CVEs most likely to be exploited to [`data/epss-top100.json`](data/epss-top100.json)
4. **Digest:** writes a readable summary to [`digests/`](digests/)
5. **History:** appends daily metrics to [`data/history.csv`](data/history.csv)
6. **README:** refreshes the summary below

The site reads the latest snapshot first, which is fast and same-origin, and falls back to the live feeds if it's missing.

Run it locally with `python3 scripts/snapshot.py` (writes files only) or `--commit` (one commit per step).

## Latest

<!-- digest:start -->
_The first snapshot will appear here after the workflow runs._
<!-- digest:end -->

---

Data: [CISA KEV](https://www.cisa.gov/known-exploited-vulnerabilities-catalog) · [FIRST EPSS](https://www.first.org/epss/). For lawful security research and authorised testing only.
