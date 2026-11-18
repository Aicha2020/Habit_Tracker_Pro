# services/habit_service.py
# Defines habit-related operations such as creation, update, deletion, and completion tracking.

from datetime import date

from storage.json_storage import load_data, save_data


def _normalize_habit_id(habit_id):
    try:
        return int(habit_id)
    except (TypeError, ValueError):
        return None


def _find_habit(habits, habit_id):
    habit_id = _normalize_habit_id(habit_id)
    if habit_id is None:
        return None
    for habit in habits:
        if habit.get('id') == habit_id:
            return habit
    return None


def _validate_name(name):
    if not isinstance(name, str) or not name.strip():
        return False
    return True


def get_all_habits():
    data = load_data()
    return data.get('habits', [])


def create_habit(name, description=''):
    if not _validate_name(name):
        return {'success': False, 'message': 'Habit name must not be empty.'}

    data = load_data()
    habits = data.setdefault('habits', [])
    next_id = 1
    if habits:
        existing_ids = [habit.get('id', 0) for habit in habits if isinstance(habit.get('id'), int)]
        next_id = max(existing_ids, default=0) + 1

    habit = {
        'id': next_id,
        'name': name.strip(),
        'description': description.strip() if isinstance(description, str) else '',
        'created_at': date.today().strftime('%Y-%m-%d'),
        'completion_dates': []
    }
    habits.append(habit)
    save_data(data)
    return {'success': True, 'message': 'Habit created successfully.', 'habit': habit}


def update_habit(habit_id, name, description=''):
    if not _validate_name(name):
        return {'success': False, 'message': 'Habit name must not be empty.'}

    data = load_data()
    habits = data.get('habits', [])
    habit = _find_habit(habits, habit_id)
    if habit is None:
        return {'success': False, 'message': 'Habit not found.'}

    habit['name'] = name.strip()
    habit['description'] = description.strip() if isinstance(description, str) else ''
    save_data(data)
    return {'success': True, 'message': 'Habit updated successfully.', 'habit': habit}


def delete_habit(habit_id):
    data = load_data()
    habits = data.get('habits', [])
    habit = _find_habit(habits, habit_id)
    if habit is None:
        return {'success': False, 'message': 'Habit not found.'}

    habits.remove(habit)
    save_data(data)
    return {'success': True, 'message': 'Habit deleted successfully.'}


def mark_habit_done(habit_id, today=None):
    if today is None:
        today = date.today()
    if isinstance(today, str):
        try:
            today = date.fromisoformat(today)
        except ValueError:
            return {'success': False, 'message': 'Invalid today date format.'}

    current_date = today.strftime('%Y-%m-%d')
    data = load_data()
    habits = data.get('habits', [])
    habit = _find_habit(habits, habit_id)
    if habit is None:
        return {'success': False, 'message': 'Habit not found.'}

    completion_dates = habit.setdefault('completion_dates', [])
    if current_date in completion_dates:
        return {'success': False, 'message': 'Habit already marked done for today.'}

    completion_dates.append(current_date)
    save_data(data)
    return {'success': True, 'message': f'Habit marked done for {current_date}.', 'habit': habit}


class HabitService:
    def get_all_habits(self):
        return get_all_habits()

    def create_habit(self, name, description=''):
        return create_habit(name, description)

    def update_habit(self, habit_id, name, description=''):
        return update_habit(habit_id, name, description)

    def delete_habit(self, habit_id):
        return delete_habit(habit_id)

    def mark_habit_done(self, habit_id, today=None):
        return mark_habit_done(habit_id, today)
