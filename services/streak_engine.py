# services/streak_engine.py
# Calculates streaks and progress for habits over time.

from datetime import date, datetime, timedelta


def calculate_current_streak(completion_dates, today=None):
    """Return the current streak length from completion date strings."""
    if today is None:
        today = date.today()

    parsed_dates = set()
    for date_text in completion_dates or []:
        try:
            parsed_date = datetime.strptime(date_text, '%Y-%m-%d').date()
            parsed_dates.add(parsed_date)
        except (ValueError, TypeError):
            continue

    if not parsed_dates:
        return 0

    sorted_dates = sorted(parsed_dates, reverse=True)
    most_recent = sorted_dates[0]

    if most_recent == today:
        streak_start = today
    elif most_recent == today - timedelta(days=1):
        streak_start = today - timedelta(days=1)
    else:
        return 0

    streak = 0
    current_day = streak_start
    for completed_day in sorted_dates:
        if completed_day == current_day:
            streak += 1
            current_day -= timedelta(days=1)
        else:
            break

    return streak


class StreakEngine:
    def calculate_streak(self, habit, date):
        # Placeholder: can be implemented using habit data and a target date.
        return calculate_current_streak(getattr(habit, 'completion_dates', []), date)

    def current_streak(self, habit):
        return calculate_current_streak(getattr(habit, 'completion_dates', []))
