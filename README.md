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
**2026-11-19**

- **KEV catalogue:** 1,786 known exploited vulnerabilities (version 2026.11.18)
- **New since last snapshot:** 4
- **Known ransomware use:** 361
- **EPSS model date:** 2026-11-19

**New since last snapshot**

| CVE | Vendor / product | Vulnerability | Added | Due | Ransomware | EPSS |
|---|---|---|---|---|---|---|
| [CVE-2024-10441](https://nvd.nist.gov/vuln/detail/CVE-2024-10441) | Synology DiskStation Manager (DSM) | Synology DiskStation Manager (DSM) Improper Encoding or Escaping of Output Vulnerability | 2026-11-18 | 2026-11-21 | Unknown | 2.1% |
| [CVE-2026-40217](https://nvd.nist.gov/vuln/detail/CVE-2026-40217) | BerriAI LiteLLM | BerriAI LiteLLM Unprotected Alternate Channel Vulnerability | 2026-11-18 | 2026-12-02 | Unknown | 61.9% |
| [CVE-2026-90817](https://nvd.nist.gov/vuln/detail/CVE-2026-90817) | Vanderbilt University Research Electronic Data Capture (REDCap) | Vanderbilt University Research Electronic Data Capture (REDCap) Code Injection Vulnerability | 2026-11-18 | 2026-11-21 | Unknown | 25.2% |
| [CVE-2026-90436](https://nvd.nist.gov/vuln/detail/CVE-2026-90436) | Apache Axis | Apache Axis Unsafe Reflection Vulnerability | 2026-11-18 | 2026-11-21 | Unknown | 1.8% |

[Full digest →](digests/2026-11-19.md) · [All digests](digests/)
<!-- digest:end -->

---

Data: [CISA KEV](https://www.cisa.gov/known-exploited-vulnerabilities-catalog) · [FIRST EPSS](https://www.first.org/epss/). For lawful security research and authorised testing only.
