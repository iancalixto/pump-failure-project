# Data dictionary: `pump_weekly_condition.csv`

One row = **one pump in one calendar week**. The fleet consists of 200 centrifugal pumps at three production
sites, monitored from 2025-01-06 to 2025-12-29 (52 weeks). The sensor columns are **weekly averages** from the
plant historian; the maintenance columns describe the state of the pump at the **end of that week**. The table
was exported from the maintenance management system on 2026-01-15.

The target `failure_next_week` says whether the pump suffered an **unplanned failure during the following week**.
In other words: everything in a row is known on Sunday evening, and the question is "will this pump fail in the
coming seven days?"

10 249 rows, 30 columns. Missing values are empty fields.

## Identifiers

| Column | Type | Description |
|---|---|---|
| `record_id` | string | Unique row identifier from the export |
| `pump_id` | string | Pump tag number (`P001` to `P200`). A pump appears in up to 52 rows |
| `week_start` | date | Monday of the week the sensor averages refer to |

## Pump master data (static, known since installation)

| Column | Unit | Description |
|---|---|---|
| `site` | - | Production site: `S1`, `S2`, `S3` |
| `fluid` | - | Pumped medium: `clean_water`, `slurry` (abrasive solids), `chemical` (hot, corrosive) |
| `rated_power_kw` | kW | Nominal motor power |
| `rated_speed_rpm` | 1/min | Nominal shaft speed (`1450` or `2950`) |
| `install_year` | year | Year the pump was commissioned |
| `duty_cycle` | - | `continuous` (runs around the clock) or `intermittent` (started and stopped on demand) |

## Operating conditions (weekly summary from the control system)

| Column | Unit | Description |
|---|---|---|
| `running_hours` | h | Hours the pump actually ran this week (max. 168) |
| `starts_count` | - | Number of motor starts this week |
| `flow_ratio_bep` | - | Mean flow divided by the flow at the best-efficiency point (BEP). 1.0 = pump runs where it was designed to run |
| `suction_pressure_bar` | bar | Mean pressure at the pump inlet (gauge). Low values mean little margin against cavitation |
| `discharge_pressure_bar` | bar | Mean pressure at the pump outlet (gauge) |
| `fluid_temp_c` | °C | Mean temperature of the pumped fluid |
| `ambient_temp_c` | °C | Mean air temperature in the pump house |
| `ambient_humidity_pct` | % | Mean relative humidity in the pump house |
| `control_valve_pos_pct` | % | Mean opening of the discharge control valve |

## Condition-monitoring sensors (weekly mean)

| Column | Unit | Description |
|---|---|---|
| `vibration_rms_mm_s` | mm/s | Overall vibration velocity (RMS) at the drive-end bearing housing. ISO 20816 zones for this pump class: < 2.8 good, 2.8-7.1 acceptable / alert, > 7.1 unacceptable. Only pumps equipped with an online accelerometer report this value |
| `bearing_temp_c` | °C | Drive-end bearing housing temperature |
| `motor_winding_temp_c` | °C | Motor stator winding temperature from the embedded RTD sensor. Not every motor has one |
| `motor_current_pct` | % of rated | Mean motor current relative to rated current |
| `seal_leak_rate_ml_h` | ml/h | Leakage collected from the mechanical-seal drain |

## Maintenance state (from the maintenance management system, end of week)

| Column | Unit | Description |
|---|---|---|
| `days_since_lubrication` | days | Days since the bearings were last re-greased |
| `weeks_since_pm` | weeks | Weeks since the last scheduled preventive maintenance (PM interval is nominally 26 weeks) |
| `hours_since_overhaul` | h | Running hours accumulated since the last overhaul or repair |
| `last_maintenance_type` | - | What the last maintenance intervention was: `preventive` (scheduled) or `corrective` (after a failure) |

## Outcome columns

| Column | Unit | Description |
|---|---|---|
| `failure_next_week` | 0/1 | **Primary target.** 1 if the pump had an unplanned failure (forced outage, emergency work order) during the following week |
| `failure_mode` | - | **Secondary target.** Root cause recorded by the technician after the repair: `bearing`, `seal`, `cavitation`, `motor`, `other`; `none` when there was no failure |
| `repair_cost_eur` | EUR | Total cost of the emergency repair booked on the work order (parts, labour, production loss). Empty when there was no failure |

## Cost figures from the maintenance department

* An **unplanned failure** costs on average **EUR 18 000** (emergency repair plus lost production).
* A **model-triggered inspection** (a technician checks the pump, re-greases, re-aligns, or schedules a planned
  seal change) costs about **EUR 1 200** and, if the pump was really about to fail, prevents the unplanned failure.
