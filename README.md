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
**2026-11-28**

- **KEV catalogue:** 1,808 known exploited vulnerabilities (version 2026.11.27)
- **New since last snapshot:** 3
- **Known ransomware use:** 362
- **EPSS model date:** 2026-11-28

**New since last snapshot**

| CVE | Vendor / product | Vulnerability | Added | Due | Ransomware | EPSS |
|---|---|---|---|---|---|---|
| [CVE-2026-120705](https://nvd.nist.gov/vuln/detail/CVE-2026-120705) | OSGeo GeoServer | OSGeo GeoServer XML Injection Vulnerability | 2026-11-27 | 2026-11-30 | Unknown | n/a |
| [CVE-2026-129243](https://nvd.nist.gov/vuln/detail/CVE-2026-129243) | OSGeo GeoServer | OSGeo GeoServer Incorrect Authorization Vulnerability | 2026-11-27 | 2026-11-30 | Unknown | n/a |
| [CVE-2026-136716](https://nvd.nist.gov/vuln/detail/CVE-2026-136716) | Drupal Core | Drupal Core Improper Check for Unusual or Exceptional Conditions Vulnerability | 2026-11-27 | 2026-11-30 | Unknown | 5.5% |

[Full digest →](digests/2026-11-28.md) · [All digests](digests/)
<!-- digest:end -->

---

Data: [CISA KEV](https://www.cisa.gov/known-exploited-vulnerabilities-catalog) · [FIRST EPSS](https://www.first.org/epss/). For lawful security research and authorised testing only.
