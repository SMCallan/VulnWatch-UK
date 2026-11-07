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
**2026-11-07**

- **KEV catalogue:** 1,769 known exploited vulnerabilities (version 2026.11.06)
- **New since last snapshot:** 1
- **Known ransomware use:** 361
- **EPSS model date:** 2026-11-06

**New since last snapshot**

| CVE | Vendor / product | Vulnerability | Added | Due | Ransomware | EPSS |
|---|---|---|---|---|---|---|
| [CVE-2026-19868](https://nvd.nist.gov/vuln/detail/CVE-2026-19868) | SonicWall SonicOS SSLVPN | SonicWall SonicOS SSLVPN Use of Single-factor Authentication Vulnerability | 2026-11-06 | 2026-11-20 | Unknown | n/a |

[Full digest →](digests/2026-11-07.md) · [All digests](digests/)
<!-- digest:end -->

---

Data: [CISA KEV](https://www.cisa.gov/known-exploited-vulnerabilities-catalog) · [FIRST EPSS](https://www.first.org/epss/). For lawful security research and authorised testing only.
