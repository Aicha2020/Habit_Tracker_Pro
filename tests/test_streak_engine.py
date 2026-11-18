# tests/test_streak_engine.py
# Unit tests for calculate_current_streak.

from datetime import date, timedelta

from services.streak_engine import calculate_current_streak


def test_no_completions_returns_zero():
    assert calculate_current_streak([]) == 0


def test_one_completion_today_returns_one():
    today = date(2026, 5, 15)
    assert calculate_current_streak(['2026-05-15'], today=today) == 1


def test_consecutive_completions_ending_today_return_correct_streak():
    today = date(2026, 5, 15)
    dates = ['2026-05-15', '2026-05-14', '2026-05-13']
    assert calculate_current_streak(dates, today=today) == 3


def test_consecutive_completions_ending_yesterday_return_correct_streak():
    today = date(2026, 5, 15)
    dates = ['2026-05-14', '2026-05-13', '2026-05-12']
    assert calculate_current_streak(dates, today=today) == 3


def test_most_recent_completion_older_than_yesterday_returns_zero():
    today = date(2026, 5, 15)
    dates = ['2026-05-13', '2026-05-12']
    assert calculate_current_streak(dates, today=today) == 0


def test_missed_day_stops_streak():
    today = date(2026, 5, 15)
    dates = ['2026-05-15', '2026-05-14', '2026-05-12']
    assert calculate_current_streak(dates, today=today) == 2


def test_duplicate_dates_do_not_increase_streak():
    today = date(2026, 5, 15)
    dates = ['2026-05-15', '2026-05-15', '2026-05-14']
    assert calculate_current_streak(dates, today=today) == 2


def test_out_of_order_dates_are_handled_correctly():
    today = date(2026, 5, 15)
    dates = ['2026-05-14', '2026-05-15', '2026-05-13']
    assert calculate_current_streak(dates, today=today) == 3


def test_invalid_date_strings_are_ignored_safely():
    today = date(2026, 5, 15)
    dates = ['2026-05-15', 'invalid-date', '2026-05-14']
    assert calculate_current_streak(dates, today=today) == 2
