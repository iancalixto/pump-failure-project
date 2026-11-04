"""Feature governance, taxonomy, and strict target leakage prevention."""

import pandas as pd


class LeakageError(ValueError):
    """Raised when data leakage or post-incident columns are detected in feature sets."""

    pass


# Primary keys and structural entity identifiers
ID_COLS: list[str] = [
    "record_id",
    "pump_id",
]

# Temporal sequencing columns
TEMPORAL_COLS: list[str] = [
    "week_start",
]

# Ground-truth prediction target
TARGET_COL: str = "failure_next_week"

# Critical target leakage: invoices and financial losses incurred retrospectively post-failure
LEAK_COLS: list[str] = [
    "repair_cost_eur",
]

# Post-incident diagnostic labels observed exclusively after failure inspection
DIAGNOSTIC_COLS: list[str] = [
    "failure_mode",
]

# Categorical operating context and equipment specifications
CATEGORICAL_FEATURES: list[str] = [
    "site",
    "fluid",
    "duty_cycle",
    "last_maintenance_type",
]

# Boolean indicators for physical sensor retrofits / presence
BOOLEAN_FEATURES: list[str] = [
    "has_vibration_sensor",
    "has_winding_temp_sensor",
]

# Quantitative sensor telemetry, design ratings, and maintenance counters
NUMERICAL_FEATURES: list[str] = [
    "rated_power_kw",
    "rated_speed_rpm",
    "install_year",
    "running_hours",
    "starts_count",
    "flow_ratio_bep",
    "suction_pressure_bar",
    "discharge_pressure_bar",
    "fluid_temp_c",
    "ambient_temp_c",
    "ambient_humidity_pct",
    "control_valve_pos_pct",
    "vibration_rms_mm_s",
    "bearing_temp_c",
    "motor_winding_temp_c",
    "motor_current_pct",
    "seal_leak_rate_ml_h",
    "days_since_lubrication",
    "weeks_since_pm",
    "hours_since_overhaul",
]

# Complete canonical list of valid features available on Sunday evening
FEATURE_COLS: list[str] = (
    NUMERICAL_FEATURES + CATEGORICAL_FEATURES + BOOLEAN_FEATURES
)


def get_feature_names() -> list[str]:
    """Return a copy of the canonical feature names list."""
    return list(FEATURE_COLS)


def get_target_name() -> str:
    """Return the primary target column name."""
    return TARGET_COL


def get_leakage_columns() -> list[str]:
    """Return a list of strictly quarantined leakage and diagnostic columns."""
    return list(LEAK_COLS + DIAGNOSTIC_COLS)


def validate_no_leakage(columns: list[str] | pd.Index) -> bool:
    """Audit a list of proposed feature column names for target leakage and post-incident attributes.

    Raises:
        LeakageError: If any target, leakage, or diagnostic column is present.
    """
    col_set = set(columns)

    for leak_col in LEAK_COLS:
        if leak_col in col_set:
            raise LeakageError(
                f"Target leakage detected! '{leak_col}' only exists post-failure and cannot be used as a predictive feature."
            )

    if TARGET_COL in col_set:
        raise LeakageError(
            f"Target column detected! '{TARGET_COL}' cannot be used as an input feature."
        )

    for diag_col in DIAGNOSTIC_COLS:
        if diag_col in col_set:
            raise LeakageError(
                f"Diagnostic post-incident attribute detected! '{diag_col}' is only known after teardown/inspection."
            )

    return True


def split_features_target(
    df: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.Series]:
    """Safely extract feature matrix X and target vector y, enforcing leakage guards.

    Args:
        df: Input dataframe containing cleaned pump telemetry records.

    Returns:
        tuple[pd.DataFrame, pd.Series]: (X, y) where X contains strictly valid Sunday-evening features
        and y contains the binary failure target.
    """
    if TARGET_COL not in df.columns:
        raise KeyError(f"Target column '{TARGET_COL}' not found in dataframe.")

    # Validate that columns to be extracted do not include leaks
    features_present = [col for col in FEATURE_COLS if col in df.columns]
    validate_no_leakage(features_present)

    X = df[features_present].copy()
    y = df[TARGET_COL].copy()

    return X, y

