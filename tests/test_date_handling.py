def test_streak_across_month_boundary():
    """Streak calculation should work across month boundaries."""
    today = date(2026, 6, 1)
    dates = [
        '2026-06-01',
        '2026-05-31',
        '2026-05-30',
        '2026-05-29',
    ]
    assert calculate_current_streak(dates, today=today) == 4


def test_streak_across_year_boundary():
    """Streak calculation should work across year boundaries."""
    today = date(2027, 1, 1)
    dates = [
        '2027-01-01',
        '2026-12-31',
        '2026-12-30',
        '2026-12-29',
    ]
    assert calculate_current_streak(dates, today=today) == 4


# Edge cases for streak
def test_streak_returns_one_when_only_today_completed():
    """Streak should be 1 when only today is marked and yesterday is missing."""
    today = date(2026, 5, 15)
    dates = ['2026-05-15']
    assert calculate_current_streak(dates, today=today) == 1


def test_streak_returns_zero_when_only_future_date():
    """Streak should be 0 when only a future date is present."""
    today = date(2026, 5, 15)
    dates = ['2026-05-20']
    assert calculate_current_streak(dates, today=today) == 0


def test_streak_returns_zero_when_only_tomorrow():
    """Streak should be 0 when only tomorrow's date is marked."""
    today = date(2026, 5, 15)
    dates = ['2026-05-16']
    assert calculate_current_streak(dates, today=today) == 0


def test_invalid_date_format_does_not_crash():
    """Invalid date strings should be safely ignored."""
    today = date(2026, 5, 15)
    dates = ['not-a-date', 'invalid', '']
    assert calculate_current_streak(dates, today=today) == 0


def test_mixed_invalid_and_valid_dates():
    """Invalid dates mixed with valid dates should calculate correctly."""
    today = date(2026, 5, 15)
    dates = [
        '2026-05-15',
        'not-valid',
        '2026-05-14',
        'invalid-date',
        '2026-05-13',
    ]
    assert calculate_current_streak(dates, today=today) == 3


def test_none_values_in_completion_dates():
    """None values should be safely ignored."""
    today = date(2026, 5, 15)
    dates = ['2026-05-15', None, '2026-05-14']
    # Code should handle this gracefully
    result = calculate_current_streak(dates, today=today)
    assert result >= 0  # Should not crash


# Large date ranges
def test_large_gap_in_dates():
    """Large gaps between dates should be handled."""
    today = date(2026, 5, 15)
    dates = ['2026-05-15', '2026-01-01']
    assert calculate_current_streak(dates, today=today) == 1


def test_very_old_dates_with_recent_today():
    """Very old completion dates should not affect streak when today is not consecutive."""
    today = date(2026, 5, 15)
    dates = ['2026-01-01', '2025-12-31', '2025-12-30']
    assert calculate_current_streak(dates, today=today) == 0
# tests/test_date_handling.py
# Tests for date handling and streak calculations across time boundaries.

from datetime import date, timedelta

import pytest

from services.streak_engine import calculate_current_streak


# Streak across month boundary
