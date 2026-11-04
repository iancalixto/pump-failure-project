# Feature Governance Register

Every column in the operational dataset is audited against the deployment condition:
**Is this value known on Sunday evening, before the upcoming operational week?**

Any feature that would not be physically or logistically available at the inference moment (Sunday 23:59) is strictly classified as **Target Leakage** or **Excluded Diagnostic** and is programmatically barred from entering training features.

---

## 1. Summary of Roles

| Role | Count | Description |
|---|---|---|
| **`id` / `temporal`** | 4 | Unique record key, pump entity identifier, or weekly timestamp. Used for joining, grouping, or temporal cross-validation splits; excluded from model feature matrix $X$. |
| **`target`** | 1 | Binary ground-truth target variable indicating whether the pump suffered an unscheduled catastrophic failure during the upcoming week. |
| **`leak`** | 1 | Post-incident information strictly generated after a failure occurs (financial repair invoices). **Never allowed in feature matrix $X$**. |
| **`excluded`** | 1 | Post-incident root cause classification (`failure_mode`) only observed following diagnostic teardown. Excluded from binary prediction. |
| **`feature` (Numerical)** | 20 | Quantitative sensor telemetry, equipment design specifications, and maintenance counters available on Sunday evening. |
| **`feature` (Categorical)** | 4 | Discrete operating properties, installation site, fluid classification, and past maintenance intervention type. |
| **`feature` (Boolean)** | 2 | Hardware configuration indicators reflecting the physical presence of sensors on each pump. |
| **Total Columns** | **32** | Verified against `data/interim/pump_clean.csv`. |

---

## 2. Complete Column Classification

| # | Column Name | Data Type | Known Sunday Evening? | Role | Rationale / Defense |
|---|---|---|---|---|---|
| 1 | `record_id` | `object` / `str` | Yes | `id` | Unique synthetic row identifier (e.g., `R100000`). Arbitrary metadata; no predictive physical meaning. |
| 2 | `pump_id` | `object` / `str` | Yes | `id` | Pump identifier (`P001` - `P200`). Used strictly for entity grouping in `GroupKFold` cross-validation to prevent same-pump data leakage between train and test sets. |
| 3 | `site` | `category` / `str` | Yes | `feature` | Facility location (`S1`, `S2`, `S3`). Fixed plant operating context, known prior to deployment. |
| 4 | `week_start` | `datetime64[ns]` | Yes | `temporal` | Calendar Monday timestamp denoting the start of the observed week. Used for temporal ordering and time-based cross-validation splits. |
| 5 | `fluid` | `category` / `str` | Yes | `feature` | Pumped medium (`clean_water`, `slurry`, `chemical`). Fixed physical operating characteristic directly impacting wear and corrosion. |
| 6 | `rated_power_kw` | `float64` | Yes | `feature` | Nameplate rated motor power in kW. Fixed engineering specification. |
| 7 | `rated_speed_rpm` | `int64` | Yes | `feature` | Nominal motor rotational velocity (e.g., 1450, 2900 RPM). Fixed engineering specification. |
| 8 | `install_year` | `int64` | Yes | `feature` | Year the pump was commissioned. Serves as a fleet aging proxy and correlates with sensor retrofit presence. |
| 9 | `duty_cycle` | `category` / `str` | Yes | `feature` | Operating profile (`continuous` vs `intermittent`). Known operational design parameter. |
| 10 | `running_hours` | `float64` | Yes | `feature` | Total operational hours accumulated by the pump during the completed week (0.0 to 168.0 hours). Logged continuously by SCADA and known at Sunday midnight. |
| 11 | `starts_count` | `int64` | Yes | `feature` | Number of motor start/stop cycles during the completed week. Direct indicator of mechanical and electrical transient stress. |
| 12 | `flow_ratio_bep` | `float64` | Yes | `feature` | Ratio of average operating flow rate to Best Efficiency Point ($Q / Q_{BEP}$). Values $< 0.7$ indicate recirculation; $> 1.15$ indicates cavitation risk. |
| 13 | `suction_pressure_bar` | `float64` | Yes | `feature` | Mean weekly inlet pressure. Low suction pressure triggers Net Positive Suction Head (NPSH) margin violations and impeller cavitation. |
| 14 | `discharge_pressure_bar`| `float64` | Yes | `feature` | Mean weekly pump head/discharge pressure. Indicates line resistance and hydraulic loading. |
| 15 | `fluid_temp_c` | `float64` | Yes | `feature` | Mean weekly process fluid temperature in Celsius. Influences seal elastomer degradation and fluid viscosity. |
| 16 | `ambient_temp_c` | `float64` | Yes | `feature` | Mean weekly site outdoor ambient temperature. Influences motor cooling efficiency. |
| 17 | `ambient_humidity_pct` | `float64` | Yes | `feature` | Mean weekly atmospheric relative humidity (0% to 100%). |
| 18 | `control_valve_pos_pct` | `float64` | Yes | `feature` | Mean control valve opening percentage (0% to 100%). Reflects throttling and operating point adjustment. |
| 19 | `vibration_rms_mm_s` | `float64` | Yes | `feature` | Weekly RMS vibration velocity (ISO 10816 severity indicator). Converted from 0.0 to `np.nan` for dropouts; structural missing for non-sensorized older pumps. |
| 20 | `bearing_temp_c` | `float64` | Yes | `feature` | Mean weekly bearing housing temperature. Elevated values indicate lubrication breakdown or bearing fatigue. |
| 21 | `motor_winding_temp_c` | `float64` | Yes | `feature` | Mean weekly stator winding temperature measured by RTD. Structural missing for older pumps without RTDs. |
| 22 | `motor_current_pct` | `float64` | Yes | `feature` | Mean motor load percentage relative to full-load current (FLC). $> 100\%$ indicates thermal overload. |
| 23 | `seal_leak_rate_ml_h` | `float64` | Yes | `feature` | Measured mechanical seal leakage rate in mL/hour. Direct pre-failure indicator for seal catastrophic blowout. |
| 24 | `days_since_lubrication`| `int64` | Yes | `feature` | Elapsed calendar days since grease renewal as of Sunday midnight. Tracks maintenance schedule compliance. |
| 25 | `weeks_since_pm` | `int64` | Yes | `feature` | Elapsed weeks since routine preventative maintenance inspection as of Sunday midnight. |
| 26 | `hours_since_overhaul` | `float64` | Yes | `feature` | Cumulative operating hours logged since last major pump rebuild. Reflects component fatigue life. |
| 27 | `last_maintenance_type`| `category` / `str` | Yes | `feature` | Categorical classification of the most recent maintenance intervention (`corrective`, `preventive`, `overhaul`, `pm`). |
| 28 | `repair_cost_eur` | `float64` | **NO** | **`leak`** | **CRITICAL TARGET LEAKAGE.** Repair invoices only exist retrospectively *after* failure occurrence (exactly 402 non-null values matching 402 failures). Strictly excluded from model feature matrix. |
| 29 | `failure_next_week` | `int64` | **NO** | **`target`** | **Primary Prediction Target.** Binary ground-truth ($y \in \{0, 1\}$) indicating whether catastrophic failure occurred during week $t+1$. |
| 30 | `failure_mode` | `category` / `str` | **NO** | **`excluded`** | Post-mortem failure classification (`bearing`, `seal`, `motor`, `cavitation`, `none`). Only identified through diagnostic inspection after failure. Excluded from binary prediction. |
| 31 | `has_vibration_sensor` | `bool` | Yes | `feature` | Hardware flag indicating whether the pump is physically equipped with an accelerometer. |
| 32 | `has_winding_temp_sensor`| `bool` | Yes | `feature` | Hardware flag indicating whether the pump is physically equipped with stator winding RTDs. |

---

## 3. Enforcement Mechanisms
1. **Programmatic Shielding:** All model feature sets must be generated through `pumpfail.features.split_features_target(df)` or validated with `pumpfail.features.validate_no_leakage(features)`.
2. **Automated Guardrail:** Any attempt to pass `repair_cost_eur` or `failure_mode` into feature matrices raises an explicit `LeakageError` terminating execution immediately.
