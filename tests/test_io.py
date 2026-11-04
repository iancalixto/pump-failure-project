"""Tests for data input/output utilities."""

from pumpfail.io import load_raw


def test_load_raw_shape():
    """Verify that the raw condition dataset loads with the expected dimensions."""
    df = load_raw()
    assert df.shape == (10249, 30)


def test_week_start_is_date():
    """Verify that week_start is parsed as datetime64 upon loading."""
    df = load_raw()
    assert str(df.week_start.dtype).startswith("datetime64")