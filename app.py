# app.py
# Entry point for Habit Tracker Pro.
# Sets up the Flask application and routes.

from datetime import date
from flask import Flask, flash, redirect, render_template, request, url_for

from services.analytics_service import get_weekly_completion_totals
from services.habit_service import HabitService
from services.streak_engine import calculate_current_streak

app = Flask(__name__)
app.secret_key = 'habit-tracker-pro-secret'

habit_service = HabitService()


def _find_habit(habit_id):
    try:
        habit_id = int(habit_id)
    except (TypeError, ValueError):
        return None

    habits = habit_service.get_all_habits()
    return next((habit for habit in habits if habit.get('id') == habit_id), None)


@app.route('/')
def dashboard():
    today = date.today()
    today_str = today.strftime('%Y-%m-%d')
    habits = habit_service.get_all_habits()

    for habit in habits:
        completion_dates = habit.get('completion_dates', [])
        habit['completed_today'] = today_str in completion_dates
        habit['current_streak'] = calculate_current_streak(completion_dates, today=today)

    analytics = get_weekly_completion_totals(habits, today=today)
    return render_template(
        'dashboard.html',
        habits=habits,
        analytics=analytics,
        today=today_str,
    )


@app.route('/habits/new')
def new_habit():
    return render_template('create_habit.html')


@app.route('/habits', methods=['POST'])
def create_habit():
    name = request.form.get('name', '')
    description = request.form.get('description', '')
    result = habit_service.create_habit(name, description)
    flash(result['message'], 'success' if result['success'] else 'error')
    return redirect(url_for('dashboard') if result['success'] else url_for('new_habit'))


@app.route('/habits/<habit_id>/edit')
def edit_habit(habit_id):
    habit = _find_habit(habit_id)
    if habit is None:
        flash('Habit not found.', 'error')
        return redirect(url_for('dashboard'))
    return render_template('edit_habit.html', habit=habit)


@app.route('/habits/<habit_id>/edit', methods=['POST'])
def update_habit(habit_id):
    name = request.form.get('name', '')
    description = request.form.get('description', '')
    result = habit_service.update_habit(habit_id, name, description)
    flash(result['message'], 'success' if result['success'] else 'error')
    return redirect(url_for('dashboard'))


@app.route('/habits/<habit_id>/delete', methods=['POST'])
def delete_habit(habit_id):
    result = habit_service.delete_habit(habit_id)
    flash(result['message'], 'success' if result['success'] else 'error')
    return redirect(url_for('dashboard'))


@app.route('/habits/<habit_id>/done', methods=['POST'])
def complete_habit(habit_id):
    result = habit_service.mark_habit_done(habit_id)
    flash(result['message'], 'success' if result['success'] else 'error')
    return redirect(url_for('dashboard'))


if __name__ == '__main__':
    app.run(debug=True)
