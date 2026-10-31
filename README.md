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
**2026-10-31**

- **KEV catalogue:** 1,766 known exploited vulnerabilities (version 2026.10.30)
- **Added in the last 7 days:** 10
- **Known ransomware use:** 361
- **EPSS model date:** 2026-10-30

**Added in the last 7 days**

| CVE | Vendor / product | Vulnerability | Added | Due | Ransomware | EPSS |
|---|---|---|---|---|---|---|
| [CVE-2026-118527](https://nvd.nist.gov/vuln/detail/CVE-2026-118527) | Ivanti Connect Secure | Ivanti Connect Secure Generation of Predictable Numbers or Identifiers Vulnerability | 2026-10-30 | 2026-11-13 | Unknown | n/a |
| [CVE-2026-111357](https://nvd.nist.gov/vuln/detail/CVE-2026-111357) | Ivanti Connect Secure | Ivanti Connect Secure Missing Authentication for Critical Function Vulnerability | 2026-10-30 | 2026-11-02 | Unknown | 0.3% |
| [CVE-2026-97229](https://nvd.nist.gov/vuln/detail/CVE-2026-97229) | GitLab Community Edition and Enterprise Edition | GitLab Community Edition and Enterprise Edition Integer Overflow or Wraparound Vulnerability | 2026-10-29 | 2026-11-01 | Unknown | 26.6% |
| [CVE-2026-76418](https://nvd.nist.gov/vuln/detail/CVE-2026-76418) | Cisco Secure Firewall ASA Software and Cisco Secure FTD Software | Cisco Secure Firewall ASA Software and Cisco Secure FTD Software Unchecked Return Value to NULL Pointer Dereference Vulnerability | 2026-10-29 | 2026-11-01 | Unknown | 0.9% |
| [CVE-2026-41709](https://nvd.nist.gov/vuln/detail/CVE-2026-41709) | Broadcom VMware ESX | Broadcom VMWare ESX Insufficient Logging Vulnerability | 2026-10-28 | 2026-11-11 | Unknown | 0.7% |
| … and 5 more | | | | | | |

[Full digest →](digests/2026-10-31.md) · [All digests](digests/)
<!-- digest:end -->

---

Data: [CISA KEV](https://www.cisa.gov/known-exploited-vulnerabilities-catalog) · [FIRST EPSS](https://www.first.org/epss/). For lawful security research and authorised testing only.
