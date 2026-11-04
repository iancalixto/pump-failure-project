"""Unit tests for data cleaning pipeline."""

import numpy as np
import pandas as pd
from pumpfail.clean import (
    add_sensor_flags,
    clean,
    drop_duplicate_pump_weeks,
    rename_record_id,
    zeros_to_nan,
)


def test_rename_record_id():
    """Verify that leading slash in /record_id is stripped."""
    df = pd.DataFrame({"/record_id": ["R1", "R2"], "val": [1, 2]})
    result = rename_record_id(df)
    assert "record_id" in result.columns
    assert "/record_id" not in result.columns


def test_drop_duplicate_pump_weeks():
    """Verify that duplicate (pump_id, week_start) rows are dropped."""
    df = pd.DataFrame(
        {
            "pump_id": ["P1", "P1", "P2"],
            "week_start": ["2025-01-06", "2025-01-06", "2025-01-06"],
            "vibration": [1.5, 1.5, 2.0],
        }
    )
    result = drop_duplicate_pump_weeks(df)
    assert len(result) == 2


def test_zeros_to_nan():
    """Verify that vibration == 0.0 is converted to NaN while keeping positive values."""
    df = pd.DataFrame({"vibration_rms_mm_s": [0.0, 1.5, np.nan, 0.0]})
    result = zeros_to_nan(df, cols=["vibration_rms_mm_s"])
    assert result["vibration_rms_mm_s"].isna().sum() == 3
    assert result["vibration_rms_mm_s"].iloc[1] == 1.5


def test_add_sensor_flags():
    """Verify that hardware sensor flags are correctly created per pump."""
    df = pd.DataFrame(
        {
            "pump_id": ["P1", "P1", "P2", "P2"],
            "vibration_rms_mm_s": [np.nan, np.nan, 1.5, 2.0],
            "motor_winding_temp_c": [70.0, 75.0, np.nan, np.nan],
        }
    )
    result = add_sensor_flags(df)
    assert "has_vibration_sensor" in result.columns
    assert "has_winding_temp_sensor" in result.columns
    # P1 has no vibration sensor, P2 has vibration sensor
    assert not result[result["pump_id"] == "P1"][
        "has_vibration_sensor"
    ].iloc[0]
    assert result[result["pump_id"] == "P2"]["has_vibration_sensor"].iloc[0]


def test_full_clean_pipeline():
    """Smoke test ensuring full clean pipeline executes seamlessly."""
    df = pd.DataFrame(
        {
            "/record_id": ["R1", "R2", "R3"],
            "pump_id": ["P1", "P1", "P2"],
            "week_start": ["2025-01-06", "2025-01-06", "2025-01-06"],
            "vibration_rms_mm_s": [0.0, 0.0, 2.5],
            "motor_winding_temp_c": [np.nan, np.nan, 80.0],
        }
    )
    result = clean(df)
    assert len(result) == 2
    assert "record_id" in result.columns
    assert result["has_vibration_sensor"].tolist() == [False, True]