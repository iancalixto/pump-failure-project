// FH Kufstein Tirol - MSc Data Science & Intelligent Analytics
// Strategy Presentation Slides - Phase 0: Data Audit and The Intern's Model
// Student / Lead Data Scientist: Ian Calixto

#set page(
  paper: "presentation-16-9",
  margin: (top: 1.2cm, bottom: 1.0cm, left: 1.4cm, right: 1.4cm),
  fill: rgb("#ffffff")
)

#set text(
  font: "Helvetica",
  size: 11pt,
  fill: rgb("#2d3748")
)

// Brand Colors
#let navy = rgb("#1a365d")
#let green = rgb("#7cb342")
#let teal = rgb("#00a3c4")
#let red = rgb("#e53e3e")
#let slate = rgb("#4a5568")
#let card-bg = rgb("#f8fafc")
#let border-color = rgb("#e2e8f0")

// Header Function for Content Slides
#let slide-header(number, title, subtitle: "") = [
  #grid(
    columns: (1fr, auto),
    gutter: 1cm,
    [
      #grid(
        columns: (auto, 1fr),
        gutter: 12pt,
        align: (top, top),
        [
          #text(size: 22pt, weight: "bold", fill: teal)[#number]
        ],
        [
          #text(size: 15pt, weight: "bold", fill: navy)[#title] \
          #if subtitle != "" [
            #text(size: 9pt, weight: "medium", fill: slate)[#subtitle]
          ]
        ]
      )
    ],
    [
      #image("presentation_assets/image1.png", width: 2.8cm)
    ]
  )
  #v(-0.15cm)
  #line(length: 100%, stroke: 0.75pt + border-color)
  #v(0.25cm)
]

// KPI Card Function
#let kpi-box(value, label, color: navy, sub: "") = {
  rect(
    fill: card-bg,
    stroke: 1pt + border-color,
    radius: 6pt,
    width: 100%,
    inset: (top: 8pt, bottom: 8pt, left: 10pt, right: 10pt)
  )[
    #text(size: 16pt, weight: "bold", fill: color)[#value] \
    #text(size: 8.5pt, weight: "bold", fill: navy)[#label]
    #if sub != "" [
      \ #text(size: 7.5pt, fill: slate)[#sub]
    ]
  ]
}

// -------------------------------------------------------------
// SLIDE 1: TITLE SLIDE (FH Kufstein Campus Layout)
// -------------------------------------------------------------

#grid(
  columns: (1.2fr, 1fr),
  gutter: 1.5cm,
  align: (horizon, horizon),
  [
    #image("presentation_assets/image1.png", width: 4.8cm)
    #v(0.5cm)
    #text(size: 10pt, weight: "bold", fill: teal)[FH KUFSTEIN TIROL | DSNSE WS 2026/27]
    #v(0.15cm)
    #text(size: 22pt, weight: "bold", fill: navy)[Pump Failure: Early Predictive Maintenance]
    #v(0.15cm)
    #text(size: 12.5pt, weight: "medium", fill: green)[Strategic Fleet Audit, Governance & Economic Modeling (Phase 0)]
    #v(0.4cm)
    #rect(fill: rgb("#edf2f7"), radius: 4pt, inset: 8pt, width: 100%)[
      #text(size: 9.5pt)[*Lead Data Scientist:* Ian Calixto \
      *Program:* MSc Data Science & Intelligent Analytics \
      *Presentation Date:* November 06, 2026]
    ]
  ],
  [
    #block(
      radius: 8pt,
      clip: true,
      stroke: 1.5pt + teal,
      inset: 0pt
    )[
      #image("presentation_assets/image2.jpg", width: 100%, fit: "cover")
    ]
  ]
)

#pagebreak()

// -------------------------------------------------------------
// SLIDE 2: THE BUSINESS PROBLEM & CONSTRAINTS
// -------------------------------------------------------------
#slide-header("01", "The Industrial Setting & Operational Reality", subtitle: "Fleet Operations, Production Costs, and Maintenance Bottlenecks")

#grid(
  columns: (1fr, 1fr, 1fr, 1fr),
  gutter: 12pt,
  kpi-box("200 Pumps", "Centrifugal Fleet", color: navy, sub: "Sites S1, S2, and S3"),
  kpi-box("52 Weeks", "Telemetry History", color: teal, sub: "10,209 valid weeks (2025)"),
  kpi-box("12 Pumps / wk", "Sunday Capacity Limit", color: red, sub: "1 technician capacity"),
  kpi-box("€18,000", "Catastrophic Failure Cost", color: red, sub: "vs €1,200 proactive inspection")
)

#v(0.3cm)

#grid(
  columns: (1.1fr, 0.9fr),
  gutter: 18pt,
  [
    #rect(fill: card-bg, stroke: 1pt + border-color, radius: 6pt, width: 100%, inset: 10pt)[
      #text(weight: "bold", fill: navy, size: 10.5pt)[The Operational Sunday-Evening Mandate:]
      - Every Sunday at 23:59, the plant manager evaluates all 200 pumps.
      - Generates *"The Sunday List"*: a prioritized schedule of at most *12 pumps*.
      - Technicians execute preventive maintenance on Monday morning.
      - Goal: Maximize catastrophic failures prevented within the strict 12-visit limit.
    ]
  ],
  [
    #rect(fill: rgb("#ebf8ff"), stroke: 1pt + rgb("#bee3f8"), radius: 6pt, width: 100%, inset: 10pt)[
      #text(weight: "bold", fill: navy, size: 10.5pt)[Asymmetric Economic Threshold:]
      $ "Threshold"^* = frac(C_"inspect", C_"fail") = frac(€1.200, €18.000) approx bold(6.67%) $
      - *Decision Rule:* Any pump exceeding *6.67% failure risk* economically justifies technician inspection!
      - Symmetric 0.5 threshold fails completely under 15:1 cost asymmetry.
    ]
  ]
)

#pagebreak()

// -------------------------------------------------------------
// SLIDE 3: DATA ENGINEERING & AUDIT (DE-03 - DE-05)
// -------------------------------------------------------------
#slide-header("02", "Empirical Data Audit & Two-Tier Pipeline", subtitle: "Eliminating SCADA Glitches, Hardware Gaps, and Sensor Dropouts")

#grid(
  columns: (1.1fr, 0.9fr),
  gutter: 16pt,
  [
    #table(
      columns: (1.4fr, 1fr, 1.6fr),
      inset: 6pt,
      stroke: (x, y) => if y == 0 { (bottom: 1.5pt + navy) } else { 0.5pt + border-color },
      fill: (x, y) => if y == 0 { rgb("#edf2f7") } else if calc.even(y) { card-bg } else { white },
      [#text(weight: "bold", size: 8pt)[Empirical Finding]],
      [#text(weight: "bold", size: 8pt)[Volume]],
      [#text(weight: "bold", size: 8pt)[Engineering Fix (DE-05)]],
      
      [`/record_id` slash], [Header], [Cleaned in `rename_record_id()`],
      [SCADA Duplicates], [40 pairs (80 rows)], [`drop_duplicates(pump_id, week)`] ,
      [Commissioning Gaps], [191 weeks (9 pumps)], [Retain active weeks (no fake rows)],
      [Hardware Sensor Absence], [25 vib / 29 RTD], [Flags: `has_vibration_sensor`],
      [Sensor 0.0 Dropouts], [94 operating rows], [Replaced `vibration == 0` with `NaN`]
    )
  ],
  [
    #rect(fill: card-bg, stroke: 1pt + border-color, radius: 6pt, width: 100%, inset: 10pt)[
      #text(weight: "bold", fill: navy, size: 10pt)[Two-Tier Architecture (Zero Leakage):]
      #v(0.15cm)
      #rect(fill: white, stroke: 0.5pt + teal, radius: 4pt, width: 100%, inset: 6pt)[
        *Tier 1 (Clean Pipeline - `src/pumpfail/clean.py`):* \
        #text(size: 8pt)[Deterministic row-level sanitation (IDs, duplicates, sensor dropouts to NaN). Exported to `data/interim/pump_clean.csv` (10,209 x 32).]
      ]
      #v(0.1cm)
      #rect(fill: white, stroke: 0.5pt + navy, radius: 4pt, width: 100%, inset: 6pt)[
        *Tier 2 (CV Estimator Pipelines):* \
        #text(size: 8pt)[Statistical imputation (median/KNN) and scaling strictly delayed into cross-validation folds. *Zero fold leakage!*]
      ]
    ]
  ]
)

#pagebreak()

// -------------------------------------------------------------
// SLIDE 4: FEATURE GOVERNANCE & LEAKAGE (DE-06)
// -------------------------------------------------------------
#slide-header("03", "Feature Governance & Quarantining Target Leakage", subtitle: "The Sunday-Evening Deployment Condition & Explicit Guardrails")

#grid(
  columns: (1fr, 1fr, 1fr),
  gutter: 12pt,
  kpi-box("26 Features", "Legitimate Predictive Predictors", color: teal, sub: "20 numeric, 4 categorical, 2 flags"),
  kpi-box("1 Target", "Ground Truth Target", color: navy, sub: "`failure_next_week` (binary 0/1)"),
  kpi-box("2 Quarantined", "Strict Leakage / Diagnostic", color: red, sub: "`repair_cost_eur`, `failure_mode`")
)

#v(0.2cm)

#grid(
  columns: (1.2fr, 0.8fr),
  gutter: 16pt,
  [
    #rect(fill: rgb("#fff5f5"), stroke: 1.5pt + red, radius: 6pt, width: 100%, inset: 10pt)[
      #text(weight: "bold", fill: red, size: 10.5pt)[The Fatal Target Leak: `repair_cost_eur`]
      - Exactly *402 non-null values* corresponding 100% to the *402 failures*.
      - Invoices only exist *post-mortem* after emergency repair teardown!
      - At Sunday 23:59, the future repair invoice does not exist.
      - Training on it creates a 100% fake "perfect" model useless in production.
    ]
  ],
  [
    #rect(fill: card-bg, stroke: 1pt + border-color, radius: 6pt, width: 100%, inset: 10pt)[
      #text(weight: "bold", fill: navy, size: 10pt)[Programmatic Guardrails:]
      - `src/pumpfail/features.py` enforces:
      ```python
      validate_no_leakage(features)
      split_features_target(df)
      ```
      - Raises `LeakageError` immediately if post-incident variables enter $X$.
    ]
  ]
)

#pagebreak()

// -------------------------------------------------------------
// SLIDE 5: CLASS IMBALANCE PROFILE (DS-01)
// -------------------------------------------------------------
#slide-header("04", "Fleet Failure Dynamics & Severe Imbalance", subtitle: "Rare-Event Characteristics Across 10,209 Operating Weeks")

#grid(
  columns: (1.05fr, 1fr),
  gutter: 14pt,
  align: (horizon, horizon),
  [
    #image("presentation_assets/fig1_imbalance.png", width: 100%)
  ],
  [
    #image("presentation_assets/fig2_site_fluid.png", width: 100%)
  ]
)

#v(0.15cm)
#rect(fill: card-bg, stroke: 0.5pt + border-color, radius: 4pt, width: 100%, inset: 6pt)[
  #text(size: 8.5pt)[*Key Takeaways:* Fleet baseline failure rate is *3.94%* (1 failure per ~25 operating weeks). Plant *S2* has the highest failure rate (*4.57%*). Fluid dynamics match engineering physics: abrasive *slurry (4.81%)* and corrosive *chemical (4.76%)* cause ~60% more failures than *clean water (2.99%)*.]
]

#pagebreak()

// -------------------------------------------------------------
// SLIDE 6: ROOT CAUSES & INFORMATION CONSTRAINTS (DS-01)
// -------------------------------------------------------------
#slide-header("05", "Failure Modes & Statistical Information Capacity", subtitle: "Effective Sample Size vs Serial Entity Autocorrelation")

#grid(
  columns: (1fr, 1.1fr),
  gutter: 16pt,
  align: (horizon, horizon),
  [
    #image("presentation_assets/fig3_failure_modes.png", width: 100%)
  ],
  [
    #rect(fill: card-bg, stroke: 1pt + border-color, radius: 6pt, width: 100%, inset: 10pt)[
      #text(weight: "bold", fill: navy, size: 10.5pt)[Statistical Information Limits ($N_"eff" << 10.209$):]
      #v(0.1cm)
      - *Mechanical Wear Dominates:* Bearings (46.5%) and Seals (25.1%) account for *71.6% of all fleet failures*. Motor coil burnout is rare (8.7%).
      - *15 Pumps (7.5%) Never Fail:* Operate 52 weeks in pristine condition; provide healthy baselines but zero pre-failure degradation signatures.
      - *Intra-Pump Autocorrelation:* 52 weeks per pump are not $i.i.d.$ observations. Random splits leak pump baseline identities!
      - *Effective Sample Size:* We only observe *402 failure transitions*.
    ]
  ]
)

#pagebreak()

// -------------------------------------------------------------
// SLIDE 7: THE INTERN'S MODEL & €7.24M FALLACY (DS-02)
// -------------------------------------------------------------
#slide-header("06", "The Intern's Fallacy: The €7.24M Catastrophe", subtitle: "Why 96.06% Accuracy Means 100% Failure to the Business")

#grid(
  columns: (1fr, 1.1fr),
  gutter: 16pt,
  align: (horizon, horizon),
  [
    #image("presentation_assets/fig4_financial_impact.png", width: 100%)
  ],
  [
    #rect(fill: rgb("#fff5f5"), stroke: 1.5pt + red, radius: 6pt, width: 100%, inset: 10pt)[
      #text(weight: "bold", fill: red, size: 11pt)[The 3 Executive Claims to Management:]
      #v(0.15cm)
      #text(size: 8.5pt)[
        1. *Claim A (The Deceptive Accuracy Trap):* Predicting that zero pumps will ever fail automatically yields *96.06% accuracy* without learning any operational signal. \
        2. *Claim B (The Operational Disaster):* At default threshold 0.5, the model detected *0 failures (Recall = 0.0%)*, sending zero technicians and causing *€7,236,000 in unmitigated outages*! \
        3. *The Resolution:* A cost-calibrated model ($tau^* approx 6.67%$) operating under the 12-inspection Sunday budget captures the catastrophic breakdowns, unlocking up to *€6.75M in annual savings*!
      ]
    ]
  ]
)

#pagebreak()

// -------------------------------------------------------------
// SLIDE 8: PHASE 1 ROADMAP
// -------------------------------------------------------------
#slide-header("07", "Phase 1 Engineering & Modeling Roadmap", subtitle: "Leakage-Free Validation, Cost Matrix, and The Sunday List")

#grid(
  columns: (1fr, 1fr, 1fr),
  gutter: 12pt,
  [
    #rect(fill: card-bg, stroke: 1pt + border-color, radius: 6pt, width: 100%, inset: 10pt, height: 100%)[
      #text(weight: "bold", fill: navy, size: 10.5pt)[1. GroupKFold Validation]
      #v(0.1cm)
      #text(size: 8.5pt)[
        - Grouped by `pump_id`.
        - Guarantees zero pumps appear simultaneously in train and test folds.
        - Evaluates generalization to unobserved machinery.
      ]
    ]
  ],
  [
    #rect(fill: card-bg, stroke: 1pt + border-color, radius: 6pt, width: 100%, inset: 10pt, height: 100%)[
      #text(weight: "bold", fill: teal, size: 10.5pt)[2. Temporal Holdout Split]
      #v(0.1cm)
      #text(size: 8.5pt)[
        - Weeks 1–39: Cross-validation training and threshold tuning.
        - Weeks 40–52 (Q4): Pure temporal holdout evaluated exactly once.
        - Prevents future look-ahead bias.
      ]
    ]
  ],
  [
    #rect(fill: card-bg, stroke: 1pt + border-color, radius: 6pt, width: 100%, inset: 10pt, height: 100%)[
      #text(weight: "bold", fill: green, size: 10.5pt)[3. Capacity Optimization]
      #v(0.1cm)
      #text(size: 8.5pt)[
        - Optimize Precision-Recall curve.
        - Sunday Top-12 ranking ($"Recall"@12$).
        - Financial cost minimization table directly in Euros (€).
      ]
    ]
  ]
)

#v(0.4cm)
#align(center)[
  #text(size: 11pt, weight: "bold", fill: navy)[Thank You! | Questions & Technical Defense] \
  #text(size: 8.5pt, fill: slate)[FH Kufstein Tirol -- Data Science & Intelligent Analytics (WS 2026/27)]
]
