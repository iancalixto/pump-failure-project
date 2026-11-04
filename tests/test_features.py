"""Unit tests for feature governance and leakage isolation."""

import pandas as pd
import pytest
from pumpfail.features import (
    BOOLEAN_FEATURES,
    CATEGORICAL_FEATURES,
    DIAGNOSTIC_COLS,
    FEATURE_COLS,
    ID_COLS,
    LEAK_COLS,
    NUMERICAL_FEATURES,
    TARGET_COL,
    TEMPORAL_COLS,
    LeakageError,
    get_feature_names,
    get_leakage_columns,
    split_features_target,
    validate_no_leakage,
)


def test_governance_constants_disjoint():
    """Verify that feature lists, leakage lists, targets, and IDs are strictly disjoint."""
    all_feature_sets = set(NUMERICAL_FEATURES) | set(CATEGORICAL_FEATURES) | set(BOOLEAN_FEATURES)
    
    # Feature list equals union of subsets
    assert set(FEATURE_COLS) == all_feature_sets
    assert len(FEATURE_COLS) == len(NUMERICAL_FEATURES) + len(CATEGORICAL_FEATURES) + len(BOOLEAN_FEATURES)
    assert len(FEATURE_COLS) == 26  # 20 num + 4 cat + 2 bool

    # Target, leaks, IDs, and diagnostics must NEVER be in FEATURE_COLS
    assert TARGET_COL not in FEATURE_COLS
    for col in LEAK_COLS:
        assert col not in FEATURE_COLS
    for col in DIAGNOSTIC_COLS:
        assert col not in FEATURE_COLS
    for col in ID_COLS:
        assert col not in FEATURE_COLS
    for col in TEMPORAL_COLS:
        assert col not in FEATURE_COLS


def test_validate_no_leakage_valid():
    """Valid feature list passes validation without raising."""
    assert validate_no_leakage(FEATURE_COLS) is True
    assert validate_no_leakage(["running_hours", "bearing_temp_c"]) is True


def test_validate_no_leakage_detects_repair_cost():
    """Attempting to use repair_cost_eur raises LeakageError."""
    with pytest.raises(LeakageError, match="Target leakage detected"):
        validate_no_leakage(["running_hours", "repair_cost_eur"])


def test_validate_no_leakage_detects_target():
    """Attempting to use the target column as a feature raises LeakageError."""
    with pytest.raises(LeakageError, match="Target column detected"):
        validate_no_leakage(["vibration_rms_mm_s", "failure_next_week"])


def test_validate_no_leakage_detects_failure_mode():
    """Attempting to use post-incident diagnostic failure_mode raises LeakageError."""
    with pytest.raises(LeakageError, match="Diagnostic post-incident"):
        validate_no_leakage(["fluid_temp_c", "failure_mode"])


def test_split_features_target():
    """Verify that split_features_target cleanly returns X (26 features) and y (target)."""
    # Create a dummy row with all 32 columns
    data = {col: [0] for col in FEATURE_COLS}
    data["record_id"] = ["R1000"]
    data["pump_id"] = ["P001"]
    data["week_start"] = ["2025-01-06"]
    data["repair_cost_eur"] = [np_nan := None]
    data["failure_mode"] = ["none"]
    data["failure_next_week"] = [0]
    
    df = pd.DataFrame(data)
    assert df.shape == (1, 32)
    
    X, y = split_features_target(df)
    
    assert X.shape == (1, 26)
    assert list(X.columns) == FEATURE_COLS
    assert y.name == "failure_next_week"
    assert len(y) == 1
    assert "repair_cost_eur" not in X.columns
    assert "failure_mode" not in X.columns
    assert "record_id" not in X.columns

