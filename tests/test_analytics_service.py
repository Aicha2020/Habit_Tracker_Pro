# tests/test_analytics_service.py
# Tests for the analytics service and weekly completion totals.

from datetime import date, timedelta

import pytest

from services.analytics_service import get_weekly_completion_totals


@pytest.fixture
def sample_habits():
    """Factory for creating sample habits."""
    def make_habit(habit_id, name, completion_dates):
        return {
            'id': habit_id,
            'name': name,
            'description': f'{name} habit',
            'created_at': '2026-05-01',
            'completion_dates': completion_dates
        }
    return make_habit


# Basic structure tests
def test_weekly_analytics_returns_seven_labels():
    """Weekly analytics should return exactly 7 labels."""
    today = date(2026, 5, 15)
    result = get_weekly_completion_totals([], today=today)
    assert len(result['labels']) == 7


def test_weekly_analytics_returns_seven_values():
    """Weekly analytics should return exactly 7 values."""
    today = date(2026, 5, 15)
    result = get_weekly_completion_totals([], today=today)
    assert len(result['values']) == 7


def test_weekly_analytics_labels_and_values_match():
    """Labels and values should have the same length."""
    today = date(2026, 5, 15)
    result = get_weekly_completion_totals([], today=today)
    assert len(result['labels']) == len(result['values'])


def test_weekly_analytics_includes_today():
    """Weekly analytics should include today's date."""
    today = date(2026, 5, 15)
    result = get_weekly_completion_totals([], today=today)
    assert result['labels'][-1] == today.isoformat()


def test_weekly_analytics_spans_seven_days():
    """Weekly analytics should span exactly 7 days starting from today - 6 days."""
    today = date(2026, 5, 15)
    result = get_weekly_completion_totals([], today=today)

    expected_start = (today - timedelta(days=6)).isoformat()
    expected_end = today.isoformat()

    assert result['labels'][0] == expected_start
    assert result['labels'][-1] == expected_end


# Data counting tests
def test_zero_completions_returns_all_zeros():
    """With no habits, all days should have 0 completions."""
    today = date(2026, 5, 15)
    result = get_weekly_completion_totals([], today=today)
    assert result['values'] == [0, 0, 0, 0, 0, 0, 0]


def test_single_completion_counted_correctly(sample_habits):
    """A single habit completion should be counted."""
    today = date(2026, 5, 15)
    habits = [sample_habits(1, 'Exercise', [today.isoformat()])]
    result = get_weekly_completion_totals(habits, today=today)

    # Last value should be 1 (today)
    assert result['values'][-1] == 1


def test_no_completions_show_zero(sample_habits):
    """Days with no completions should return 0."""
    today = date(2026, 5, 15)
    habits = [sample_habits(1, 'Exercise', [])]
    result = get_weekly_completion_totals(habits, today=today)

    assert all(v == 0 for v in result['values'])


def test_multiple_habits_same_date_increase_total(sample_habits):
    """Multiple habits completed on the same date should increase that date's total."""
    today = date(2026, 5, 15)
    habits = [
        sample_habits(1, 'Exercise', [today.isoformat()]),
        sample_habits(2, 'Read', [today.isoformat()]),
        sample_habits(3, 'Meditate', [today.isoformat()])
    ]
    result = get_weekly_completion_totals(habits, today=today)

    # Last value should be 3 (all habits completed today)
    assert result['values'][-1] == 3


def test_same_habit_multiple_dates(sample_habits):
    """Same habit completed on multiple dates should increment each date."""
    today = date(2026, 5, 15)
    yesterday = (today - timedelta(days=1)).isoformat()
    today_str = today.isoformat()

    habits = [sample_habits(1, 'Exercise', [today_str, yesterday])]
    result = get_weekly_completion_totals(habits, today=today)

    # Last 2 values should be 1 each
    assert result['values'][-1] == 1  # Today
    assert result['values'][-2] == 1  # Yesterday


def test_duplicate_completion_dates_counted_once(sample_habits):
    """Duplicate completion dates from same habit should be counted properly."""
    today = date(2026, 5, 15)
    # Note: duplicates shouldn't occur in normal usage, but system should handle gracefully
    habits = [sample_habits(1, 'Exercise', [today.isoformat(), today.isoformat()])]
    result = get_weekly_completion_totals(habits, today=today)

    # Duplicate dates for the same habit should be counted once
    assert result['values'][-1] == 1


def test_completions_outside_week_not_counted(sample_habits):
    """Completions outside the last 7 days should not be counted."""
    today = date(2026, 5, 15)
    week_ago = (today - timedelta(days=7)).isoformat()
    two_weeks_ago = (today - timedelta(days=14)).isoformat()

    habits = [sample_habits(1, 'Exercise', [week_ago, two_weeks_ago])]
    result = get_weekly_completion_totals(habits, today=today)

    assert all(v == 0 for v in result['values'])


def test_completion_at_boundary_of_week_included(sample_habits):
    """Completions at day 0 of the week (6 days ago) should be counted."""
    today = date(2026, 5, 15)
    six_days_ago = (today - timedelta(days=6)).isoformat()

    habits = [sample_habits(1, 'Exercise', [six_days_ago])]
    result = get_weekly_completion_totals(habits, today=today)

    # First value should be 1
    assert result['values'][0] == 1


# Edge cases and robustness
def test_handles_none_habits_list():
    """Should handle None as habits list gracefully."""
    today = date(2026, 5, 15)
    result = get_weekly_completion_totals(None, today=today)
    assert all(v == 0 for v in result['values'])


def test_handles_habit_with_empty_completion_dates(sample_habits):
    """Should handle habits with missing completion_dates key."""
    today = date(2026, 5, 15)
    habit = sample_habits(1, 'Exercise', [])
    del habit['completion_dates']

    result = get_weekly_completion_totals([habit], today=today)
    assert all(v == 0 for v in result['values'])


def test_handles_invalid_date_strings(sample_habits):
    """Should handle invalid date strings gracefully."""
    today = date(2026, 5, 15)
    habits = [sample_habits(1, 'Exercise', ['invalid-date', 'not-a-date'])]

    # Should not crash
    result = get_weekly_completion_totals(habits, today=today)
    assert all(v == 0 for v in result['values'])


def test_weekly_analytics_consistency_across_calls(sample_habits):
    """Multiple calls with same data should produce same result."""
    today = date(2026, 5, 15)
    habits = [
        sample_habits(1, 'Exercise', [today.isoformat()]),
        sample_habits(2, 'Read', [(today - timedelta(days=1)).isoformat()])
    ]

    result1 = get_weekly_completion_totals(habits, today=today)
    result2 = get_weekly_completion_totals(habits, today=today)

    assert result1 == result2
