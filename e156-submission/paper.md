Mahmood Ahmad
Tahir Heart Institute
mahmood.ahmad2@nhs.net

MetaGuard: A Browser-Based Robust and Forensic Meta-Analysis Toolkit

Does a browser tool integrating density-power-divergence robust pooling, right-truncated meta-analysis for p-hacking detection, and precision-weighted random forests improve meta-analysis robustness assessment? The toolkit was developed and validated on simulated datasets with known outliers, truncated p-value distributions, and moderator-driven heterogeneity across 22 integration tests. Each engine operates independently: DPD iterative reweighting for outlier downweighting, EM-based z-score truncation modeling for selective reporting, and precision-weighted bagged trees for heterogeneity explanation. DPD robust pooling at alpha 0.5 reduced pooled MD bias by 52% versus standard inverse-variance estimation, with 95% CI excluding contaminated values. All 22 Selenium tests passed, confirming alpha-zero DPD equivalence to maximum likelihood, RTMA correction of affirmative-result truncation, and stable MetaForest variable importance rankings. MetaGuard provides the first zero-dependency browser implementation of three frontier robustness methods previously requiring R or Python installations. The tool is limited to continuous outcomes for the robust and RTMA engines, and MetaForest reliability may diminish when fewer than ten moderator-annotated studies are available.

Outside Notes

Type: methods
Primary estimand: Outlier-adjusted pooled effect via DPD
App: MetaGuard v2.0.0
Data: Simulated meta-analysis datasets with known outliers and p-hacking
Code: https://github.com/mahmood726-cyber/metaguard
Version: 2.0.0
Certainty: moderate
Validation: DRAFT

References

1. Carlisle JB. Data fabrication and other reasons for non-random sampling in 5087 randomised, controlled trials in anaesthetic and general medical journals. Anaesthesia. 2017;72(8):944-952.
2. Brown NJL, Heathers JAJ. The GRIM test: a simple technique detects numerous anomalies in the reporting of results in psychology. Soc Psychol Personal Sci. 2017;8(4):363-369.
3. Borenstein M, Hedges LV, Higgins JPT, Rothstein HR. Introduction to Meta-Analysis. 2nd ed. Wiley; 2021.
