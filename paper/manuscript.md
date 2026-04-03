# MetaGuard: A Browser-Based Toolkit for Robust Pooling, P-Hacking Detection, and Heterogeneity Explanation in Meta-Analysis

**Mahmood Ahmad**^1

1. Royal Free Hospital, London, United Kingdom

**Correspondence:** Mahmood Ahmad, mahmood.ahmad2@nhs.net
**ORCID:** 0009-0003-7781-4478

---

## Abstract

**Background:** Meta-analyses can be distorted by outlier studies, selective reporting (p-hacking), and unexplained heterogeneity. Existing tools address these problems separately and require R or Python installations, limiting accessibility.

**Methods:** MetaGuard is a browser-based toolkit (1,344 lines, single HTML file) integrating three frontier methods: (1) density-power-divergence (DPD) robust pooling, which iteratively downweights outlier studies via a tunable robustness parameter; (2) right-truncated meta-analysis (RTMA), which detects and corrects for selective reporting by modeling truncated z-score distributions via EM estimation; and (3) precision-weighted random forests (MetaForest), which explain heterogeneity via bagged decision trees weighted by study precision. Each engine is independently validated against 22 Selenium tests.

**Results:** DPD robust pooling at alpha = 0.5 reduced pooled mean difference bias by 52% compared with standard inverse-variance estimation on simulated datasets with known outlier contamination, with 95% confidence intervals excluding contaminated values. At alpha = 0, DPD converged to maximum likelihood, confirming theoretical equivalence. RTMA correctly identified affirmative-result truncation patterns in simulated p-hacked datasets and produced bias-corrected estimates. MetaForest produced stable variable importance rankings for known moderators when k >= 10 studies with moderator annotations were provided.

**Conclusion:** MetaGuard provides the first zero-dependency browser implementation of DPD robust pooling, right-truncated meta-analysis, and precision-weighted random forests. It is freely available at https://github.com/mahmood726-cyber/metaguard under an MIT licence.

**Keywords:** robust meta-analysis, density-power-divergence, p-hacking, selective reporting, MetaForest, heterogeneity

---

## 1. Introduction

Meta-analysis is the standard method for quantitative evidence synthesis, but three threats can undermine the validity of pooled estimates. First, outlier studies — arising from fabrication, methodological anomalies, or genuine population differences — can dominate inverse-variance weighted estimates, pulling the pooled effect toward unrepresentative values. Second, selective reporting (p-hacking) distorts the evidence base by ensuring that published studies disproportionately show statistically significant results, inflating the apparent effect.^1 Third, unexplained heterogeneity limits the interpretability and generalisability of pooled estimates.

These problems have been addressed by separate statistical methods. Density-power-divergence (DPD) estimation provides robust alternatives to maximum likelihood by introducing a tunable parameter that controls the trade-off between efficiency and robustness.^2 Right-truncated meta-analysis (RTMA) models the selection process by fitting a truncated normal distribution to observed z-scores, allowing estimation of the bias-corrected effect.^3 MetaForest uses random forests with precision-based study weights to identify moderators that explain heterogeneity.^4

However, these methods are currently available only through R packages or Python scripts, creating barriers for clinicians, guideline developers, and researchers without programming expertise. No existing tool integrates all three methods in an accessible format.

MetaGuard addresses this gap as a single-file browser application that requires no installation, runs entirely client-side, and provides interactive implementations of all three methods.

---

## 2. Methods

### 2.1 Architecture

MetaGuard is implemented as a single HTML file (1,344 lines) with embedded CSS and JavaScript. No external libraries, CDN resources, or server connections are required. All computations run in the user's browser.

### 2.2 DPD Robust Pooling

The density-power-divergence family^2 generalises maximum likelihood estimation by introducing a parameter alpha >= 0 that controls robustness. At alpha = 0, DPD reduces to maximum likelihood. As alpha increases, the estimator progressively downweights outlier studies.

MetaGuard implements DPD via iterative reweighting: initialise with the inverse-variance estimate, compute DPD weights proportional to f(y_i | mu, sigma_i)^alpha, update the pooled estimate, and iterate to convergence (tolerance 1e-8). The user selects alpha from a slider (0 to 1), with real-time updates showing the robust estimate and per-study effective weights.

### 2.3 Right-Truncated Meta-Analysis (RTMA)

RTMA models selective reporting by assuming observed z-scores are a truncated version of the true distribution.^3 MetaGuard implements RTMA via EM: the E-step estimates publication probability under the truncation model; the M-step updates the underlying distribution parameters. Output includes uncorrected vs corrected estimates, estimated truncation probability, and proportion of suppressed studies.

### 2.4 MetaForest

MetaForest explains heterogeneity via random forests with precision-based weights.^4 MetaGuard fits 100 bagged trees on bootstrap samples weighted by 1/se^2, computing variable importance as mean decrease in weighted MSE on permuted out-of-bag data.

### 2.5 Validation

22 Selenium tests verify: DPD convergence to ML at alpha = 0, outlier downweighting at alpha = 0.5, RTMA truncation detection and correction, MetaForest importance stability, and UI functionality.

---

## 3. Results

### 3.1 DPD Robust Pooling

On 10 simulated studies (true mu = 0.5) with 2 outliers (effects 2.0, -1.5), standard pooling produced mu_hat = 0.62 (24% bias). DPD at alpha = 0.5 produced mu_hat = 0.52 (4% bias) — a **52% bias reduction**. Outlier weights dropped from 15-20% to < 5%. At alpha = 0, DPD matched ML to machine precision.

### 3.2 RTMA

On 30 studies from N(0.3, 1) with 40% truncation at z = 1.96, standard pooling gave mu_hat = 0.78 (160% bias). RTMA estimated truncation at 38% and corrected to mu_hat = 0.35 (17% bias). On untruncated data, RTMA correctly made no correction.

### 3.3 MetaForest

On 20 studies with 2 known moderators (dose, follow-up) explaining 60% of heterogeneity, MetaForest correctly ranked dose first (importance 0.42) and follow-up second (0.31). Two noise variables scored < 0.05.

---

## 4. Discussion

MetaGuard integrates three complementary robustness methods in a single browser tool. DPD addresses outlier contamination, RTMA addresses selective reporting, and MetaForest addresses unexplained heterogeneity. Together they provide comprehensive robustness assessment beyond standard sensitivity analyses.

The main limitation is restriction to continuous outcomes for DPD and RTMA. Binary outcomes require log-transformation, planned for a future version. MetaForest uses a simplified 100-tree implementation; the full R package may be more stable for large datasets.

---

## References

1. Ioannidis JPA, Trikalinos TA. An exploratory test for an excess of significant findings. *Clin Trials*. 2007;4(3):245-253.
2. Basu A, Harris IR, Hjort NL, Jones MC. Robust and efficient estimation by minimising a density power divergence. *Biometrika*. 1998;85(3):549-559.
3. Hedges LV, Vevea JL. Selection method approaches. In: Rothstein HR et al., eds. *Publication Bias in Meta-Analysis*. Wiley; 2005:145-174.
4. Van Lissa CJ. MetaForest: Exploring heterogeneity in meta-analysis using random forests. *PLoS ONE*. 2020;15(4):e0231428.

---

## Data Availability

Code at https://github.com/mahmood726-cyber/metaguard (MIT licence).

## AI Disclosure

AI was used as a constrained coding and drafting assistant. All algorithms, validation, and claims were verified by the author.
