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
**2026-11-26**

- **KEV catalogue:** 1,805 known exploited vulnerabilities (version 2026.11.25)
- **New since last snapshot:** 10
- **Known ransomware use:** 362
- **EPSS model date:** 2026-11-26

**New since last snapshot**

| CVE | Vendor / product | Vulnerability | Added | Due | Ransomware | EPSS |
|---|---|---|---|---|---|---|
| [CVE-2026-103406](https://nvd.nist.gov/vuln/detail/CVE-2026-103406) | Hewlett Packard Enterprise (HPE) Juniper Session Smart Conductor and Session Smart Router | Hewlett Packard Enterprise (HPE) Juniper Session Smart Conductor and Session Smart Router OS Command Injection Vulnerability | 2026-11-25 | 2026-11-28 | Unknown | 1.5% |
| [CVE-2026-133469](https://nvd.nist.gov/vuln/detail/CVE-2026-133469) | Vates Xen Orchestra | Vates Xen Orchestra Improper Validation of Specified Type of Input Vulnerability | 2026-11-25 | 2026-11-28 | Unknown | 31.8% |
| [CVE-2025-41450](https://nvd.nist.gov/vuln/detail/CVE-2025-41450) | Danfoss AK-SM 800A Series | Danfoss AK-SM 800A Series Improper Authentication Vulnerability | 2026-11-25 | 2026-12-09 | Unknown | 4.3% |
| [CVE-2023-25914](https://nvd.nist.gov/vuln/detail/CVE-2023-25914) | Danfoss AK-SM 800A Series | Danfoss AK-SM 800A Series Path Traversal Vulnerability | 2026-11-25 | 2026-11-28 | Unknown | 1.8% |
| [CVE-2023-25915](https://nvd.nist.gov/vuln/detail/CVE-2023-25915) | Danfoss AK-SM 800A Series | Danfoss AK-SM 800A Series Improper Input Validation Vulnerability | 2026-11-25 | 2026-11-28 | Unknown | 2.5% |
| … and 5 more | | | | | | |

[Full digest →](digests/2026-11-26.md) · [All digests](digests/)
<!-- digest:end -->

---

Data: [CISA KEV](https://www.cisa.gov/known-exploited-vulnerabilities-catalog) · [FIRST EPSS](https://www.first.org/epss/). For lawful security research and authorised testing only.
