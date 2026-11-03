# Pump Failure: Early Imbalanced Predictive Maintenance

Academic and applied predictive maintenance project for **DSNSE (Data Science in Natural Sciences and Engineering) - WS 2026/27**, FH Kufstein Tirol.

---

## 1. Executive Summary & Problem Framing
This project addresses predictive maintenance across an industrial fleet of **200 centrifugal pumps** operating across 3 manufacturing sites over 52 weeks of operation. 

Every Monday morning (evaluated on Sunday night), the plant operations manager requires an actionable prioritized inspection schedule ("Sunday List"):
* **Target:** Predict whether a pump will suffer an operational failure in the upcoming week (`failure_next_week`).
* **Imbalance Profile:** Rare-event operational regime with approximately **~4% positive failure rate**.
* **Operational Constraint:** Strict maintenance capacity limit of **at most 12 inspections per week** (or 24 with a secondary maintenance technician).

---

## 2. Economic Cost Matrix
Decisions are driven by total operational cost rather than unweighted classification metrics (e.g., accuracy or raw F1-score at 0.5):
* **Unplanned Failure Cost:** **€18,000** (critical outage, production stoppage, severe damage).
* **Proactive Inspection Cost:** **€1,200** (prevents the failure if scheduled prior to breakdown).
* **Theoretical Cost Threshold:**
  $$\text{Threshold}^* \approx \frac{C_{\text{inspect}}}{C_{\text{fail}}} = \frac{1,200}{18,000} \approx 6.67\%$$

---

## 3. Engineering & Modeling Principles
1. **Leakage Prevention:** Strict feature governance. Retrospective post-failure columns (e.g. `repair_cost_eur`, `failure_mode`) are isolated and excluded from training.
2. **Honest Validation Hierarchy:**
   * **GroupKFold (by `pump_id`):** Prevents pump-identity leakage across folds.
   * **Temporal Split:** Weeks 1–39 strictly for training and validation out-of-fold tuning; Weeks 40–52 preserved as an untouched holdout evaluated exactly once.
3. **Reproducibility & Code Standards:** Managed with `uv`, atomic commits (`feat:`, `chore:`, `test:`, `docs:`), and full Test-Driven Development (TDD).

---

## 4. Project Structure (Overview)
```text
pump-failure-project/
├── data/               # raw and interim data (git-ignored)
├── docs/               # Architecture decisions (DECISIONS.md) & Governance
├── notebooks/          # Step-by-step reproducible laboratory notebooks
├── src/pumpfail/       # Modular, unit-tested core logic
├── tests/              # Pytest test suite
└── pyproject.toml      # Project metadata and dependencies (uv)
```

