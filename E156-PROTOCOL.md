# E156 Protocol — `MetaGuard`

This repository is the source code and dashboard backing an E156 micro-paper on the [E156 Student Board](https://mahmood726-cyber.github.io/e156/students.html).

---

## `[96]` MetaGuard: A Browser-Based Robust and Forensic Meta-Analysis Toolkit

**Type:** methods  |  ESTIMAND: Outlier-adjusted pooled effect via DPD  
**Data:** Simulated meta-analysis datasets with known outliers and p-hacking

### 156-word body

Does a browser tool integrating density-power-divergence robust pooling, right-truncated meta-analysis for p-hacking detection, and precision-weighted random forests improve meta-analysis robustness assessment? The toolkit was developed and validated on simulated datasets with known outliers, truncated p-value distributions, and moderator-driven heterogeneity across 22 integration tests. Each engine operates independently: DPD iterative reweighting for outlier downweighting, EM-based z-score truncation modeling for selective reporting, and precision-weighted bagged trees for heterogeneity explanation. DPD robust pooling at alpha 0.5 reduced pooled MD bias by 52% versus standard inverse-variance estimation, with 95% CI excluding contaminated values. All 22 Selenium tests passed, confirming alpha-zero DPD equivalence to maximum likelihood, RTMA correction of affirmative-result truncation, and stable MetaForest variable importance rankings. MetaGuard provides the first zero-dependency browser implementation of three frontier robustness methods previously requiring R or Python installations. The tool is limited to continuous outcomes for the robust and RTMA engines, and MetaForest reliability may diminish when fewer than ten moderator-annotated studies are available.

### Submission metadata

```
Corresponding author: Mahmood Ahmad <mahmood.ahmad2@nhs.net>
ORCID: 0000-0001-9107-3704
Affiliation: Tahir Heart Institute, Rabwah, Pakistan

Links:
  Code:      https://github.com/mahmood726-cyber/MetaGuard
  Protocol:  https://github.com/mahmood726-cyber/MetaGuard/blob/main/E156-PROTOCOL.md
  Dashboard: https://mahmood726-cyber.github.io/metaguard/

References (topic pack: heterogeneity / prediction interval):
  1. Higgins JPT, Thompson SG. 2002. Quantifying heterogeneity in a meta-analysis. Stat Med. 21(11):1539-1558. doi:10.1002/sim.1186
  2. IntHout J, Ioannidis JP, Rovers MM, Goeman JJ. 2016. Plea for routinely presenting prediction intervals in meta-analysis. BMJ Open. 6(7):e010247. doi:10.1136/bmjopen-2015-010247

Data availability: No patient-level data used. Analysis derived exclusively
  from publicly available aggregate records. All source identifiers are in
  the protocol document linked above.

Ethics: Not required. Study uses only publicly available aggregate data; no
  human participants; no patient-identifiable information; no individual-
  participant data. No institutional review board approval sought or required
  under standard research-ethics guidelines for secondary methodological
  research on published literature.

Funding: None.

Competing interests: MA serves on the editorial board of Synthēsis (the
  target journal); MA had no role in editorial decisions on this
  manuscript, which was handled by an independent editor of the journal.

Author contributions (CRediT):
  [STUDENT REWRITER, first author] — Writing – original draft, Writing –
    review & editing, Validation.
  [SUPERVISING FACULTY, last/senior author] — Supervision, Validation,
    Writing – review & editing.
  Mahmood Ahmad (middle author, NOT first or last) — Conceptualization,
    Methodology, Software, Data curation, Formal analysis, Resources.

AI disclosure: Computational tooling (including AI-assisted coding via
  Claude Code [Anthropic]) was used to develop analysis scripts and assist
  with data extraction. The final manuscript was human-written, reviewed,
  and approved by the author; the submitted text is not AI-generated. All
  quantitative claims were verified against source data; cross-validation
  was performed where applicable. The author retains full responsibility for
  the final content.

Preprint: Not preprinted.

Reporting checklist: PRISMA 2020 (methods-paper variant — reports on review corpus).

Target journal: ◆ Synthēsis (https://www.synthesis-medicine.org/index.php/journal)
  Section: Methods Note — submit the 156-word E156 body verbatim as the main text.
  The journal caps main text at ≤400 words; E156's 156-word, 7-sentence
  contract sits well inside that ceiling. Do NOT pad to 400 — the
  micro-paper length is the point of the format.

Manuscript license: CC-BY-4.0.
Code license: MIT.

SUBMITTED: [ ]
```


---

_Auto-generated from the workbook by `C:/E156/scripts/create_missing_protocols.py`. If something is wrong, edit `rewrite-workbook.txt` and re-run the script — it will overwrite this file via the GitHub API._