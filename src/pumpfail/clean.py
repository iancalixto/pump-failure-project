"""Data cleaning pipeline for weekly pump operational condition records."""

import numpy as np
import pandas as pd


def rename_record_id(df: pd.DataFrame) -> pd.DataFrame:
    """Strip leading slash from '/record_id' column if present."""
    df = df.copy()
    if "/record_id" in df.columns:
        df = df.rename(columns={"/record_id": "record_id"})
    return df


def drop_duplicate_pump_weeks(df: pd.DataFrame) -> pd.DataFrame:
    """Remove redundant duplicate records for the same pump and week."""
    df = df.copy()
    if "pump_id" in df.columns and "week_start" in df.columns:
        df = df.drop_duplicates(subset=["pump_id", "week_start"], keep="first")
    return df


def zeros_to_nan(
    df: pd.DataFrame, cols: list[str] | None = None
) -> pd.DataFrame:
    """Convert impossible sensor zeros (telemetry dropouts) to NaN."""
    df = df.copy()
    if cols is None:
        cols = ["vibration_rms_mm_s"]

    for col in cols:
        if col in df.columns:
            df.loc[df[col] == 0.0, col] = np.nan
    return df


def add_sensor_flags(df: pd.DataFrame) -> pd.DataFrame:
    """Create boolean indicators indicating structural presence of physical sensors per pump."""
    df = df.copy()

    # Vibration sensor availability flag
    if "vibration_rms_mm_s" in df.columns and "pump_id" in df.columns:
        has_vib = df.groupby("pump_id")["vibration_rms_mm_s"].transform(
            lambda s: s.notna().any()
        )
        df["has_vibration_sensor"] = has_vib

    # Motor winding temperature sensor availability flag
    if "motor_winding_temp_c" in df.columns and "pump_id" in df.columns:
        has_winding = df.groupby("pump_id")["motor_winding_temp_c"].transform(
            lambda s: s.notna().any()
        )
        df["has_winding_temp_sensor"] = has_winding

    return df


def clean(df: pd.DataFrame) -> pd.DataFrame:
    """Execute the full canonical data cleaning pipeline using method chaining."""
    return (
        df.pipe(rename_record_id)
        .pipe(drop_duplicate_pump_weeks)
        .pipe(zeros_to_nan, cols=["vibration_rms_mm_s"])
        .pipe(add_sensor_flags)
    )

    