"""Data ingestion utilities for the pump failure project."""

from pathlib import Path
import pandas as pd

# Automatically resolves the project root regardless of execution directory
ROOT = Path(__file__).resolve().parents[2]
RAW_PATH = ROOT / "data" / "raw" / "pump_weekly_condition.csv"


def load_raw(path: Path = RAW_PATH) -> pd.DataFrame:
    """Load the raw weekly pump condition dataset with canonical date parsing.

    Parameters
    ----------
    path : Path, optional
        Path to the raw CSV file. Defaults to data/raw/pump_weekly_condition.csv.

    Returns
    -------
    pd.DataFrame
        Uncleaned raw dataset with week_start parsed as datetime64.
    """
    return pd.read_csv(path, parse_dates=["week_start"])