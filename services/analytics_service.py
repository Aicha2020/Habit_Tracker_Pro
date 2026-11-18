# services/analytics_service.py
# Provides analytics data derived from habits and streaks.

from datetime import date, timedelta


def get_weekly_completion_totals(habits, today=None):
    """Return labels and values for the last 7 days of habit completions."""
    if today is None:
        today = date.today()
    elif isinstance(today, str):
        today = date.fromisoformat(today)

    last_seven = [(today - timedelta(days=day)).isoformat() for day in reversed(range(7))]
    totals = {day: 0 for day in last_seven}

    for habit in habits or []:
        # Count each completion date once per habit (deduplicate per habit)
        for completion_date in set(habit.get('completion_dates', []) or []):
            if completion_date in totals:
                totals[completion_date] += 1

    return {
        'labels': last_seven,
        'values': [totals[day] for day in last_seven]
    }


class AnalyticsService:
    def summary(self, habits):
        return {'weekly_completion_totals': get_weekly_completion_totals(habits)}

    def streak_trends(self, habits):
        return get_weekly_completion_totals(habits)
