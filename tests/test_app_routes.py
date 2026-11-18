# tests/test_app_routes.py
# Comprehensive integration tests for Habit Tracker Pro Flask routes.

import json
from datetime import date

import pytest

from app import app
import storage.json_storage as json_storage
from storage.json_storage import load_data


def create_habit(client, name='Read books', description='Daily reading'):
    return client.post(
        '/habits',
        data={'name': name, 'description': description},
        follow_redirects=True,
    )


@pytest.fixture
def client(tmp_path, monkeypatch):
    temp_file = tmp_path / 'habits.json'
    monkeypatch.setattr(json_storage, 'DATA_PATH', str(temp_file))
    with app.test_client() as client:
        yield client


# Basic route tests
def test_get_home_returns_200(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Habit Tracker Pro' in response.data


def test_get_new_habit_form_returns_200(client):
    response = client.get('/habits/new')
    assert response.status_code == 200
    assert b'Create Habit' in response.data


# Create habit tests
def test_create_habit_redirects_and_stores_habit(client):
    response = create_habit(client, name='Workout', description='Morning exercise')
    assert response.status_code == 200
    assert b'Workout' in response.data
    assert b'Habit created successfully' in response.data

    data = load_data()
    assert len(data['habits']) == 1
    assert data['habits'][0]['name'] == 'Workout'
    assert data['habits'][0]['description'] == 'Morning exercise'


def test_create_habit_with_empty_name_fails(client):
    response = create_habit(client, name='', description='Some description')
    assert response.status_code == 200
    assert b'Habit name must not be empty' in response.data

    data = load_data()
    assert len(data['habits']) == 0


def test_create_habit_with_whitespace_only_name_fails(client):
    response = create_habit(client, name='   ', description='Some description')
    assert response.status_code == 200
    assert b'Habit name must not be empty' in response.data

    data = load_data()
    assert len(data['habits']) == 0


def test_create_habit_with_empty_description(client):
    response = create_habit(client, name='Exercise', description='')
    assert response.status_code == 200
    assert b'Habit created successfully' in response.data

    data = load_data()
    assert len(data['habits']) == 1
    assert data['habits'][0]['description'] == ''


# Edit habit tests
def test_edit_habit_form_displays(client):
    create_habit(client, name='Read', description='Read books')
    data = load_data()
    habit_id = data['habits'][0]['id']

    response = client.get(f'/habits/{habit_id}/edit')
    assert response.status_code == 200
    assert b'Edit Habit' in response.data
    assert b'Read' in response.data


def test_edit_habit_updates_name_and_description(client):
    create_habit(client, name='Read', description='Read books')
    data = load_data()
    habit_id = data['habits'][0]['id']

    response = client.post(
        f'/habits/{habit_id}/edit',
        data={'name': 'Exercise', 'description': 'Workout'},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b'Habit updated successfully' in response.data

    data = load_data()
    assert data['habits'][0]['name'] == 'Exercise'
    assert data['habits'][0]['description'] == 'Workout'


def test_edit_habit_with_empty_name_fails(client):
    create_habit(client, name='Read')
    data = load_data()
    habit_id = data['habits'][0]['id']

    response = client.post(
        f'/habits/{habit_id}/edit',
        data={'name': '', 'description': 'New desc'},
        follow_redirects=True,
    )
    assert b'Habit name must not be empty' in response.data

    data = load_data()
    assert data['habits'][0]['name'] == 'Read'


def test_edit_missing_habit_id_shows_error(client):
    response = client.get('/habits/9999/edit', follow_redirects=True)
    assert response.status_code == 200
    assert b'Habit not found' in response.data


def test_edit_invalid_habit_id_shows_error(client):
    response = client.get('/habits/invalid/edit', follow_redirects=True)
    assert response.status_code == 200
    assert b'Habit not found' in response.data


# Dashboard tests
def test_dashboard_displays_created_habit(client):
    create_habit(client, name='Meditate', description='Evening mindfulness')
    response = client.get('/')
    assert response.status_code == 200
    assert b'Meditate' in response.data
    assert b'Evening mindfulness' in response.data


def test_dashboard_shows_multiple_habits(client):
    create_habit(client, name='Read')
    create_habit(client, name='Exercise')
    create_habit(client, name='Meditate')

    response = client.get('/')
    assert response.status_code == 200
    assert b'Read' in response.data
    assert b'Exercise' in response.data
    assert b'Meditate' in response.data


# Mark done tests
def test_mark_habit_done_stores_today_completion(client):
    create_habit(client, name='Journal', description='Write daily notes')
    data = load_data()
    habit_id = data['habits'][0]['id']

    response = client.post(f'/habits/{habit_id}/done', follow_redirects=True)
    assert response.status_code == 200
    assert b'Habit marked done' in response.data

    data = load_data()
    completions = data['habits'][0]['completion_dates']
    assert completions == [date.today().isoformat()]


def test_mark_habit_done_twice_does_not_duplicate(client):
    create_habit(client, name='Stretch', description='Quick stretch')
    data = load_data()
    habit_id = data['habits'][0]['id']

    client.post(f'/habits/{habit_id}/done', follow_redirects=True)
    response = client.post(f'/habits/{habit_id}/done', follow_redirects=True)
    assert response.status_code == 200
    assert b'already marked done for today' in response.data.lower()

    data = load_data()
    completions = data['habits'][0]['completion_dates']
    assert completions == [date.today().isoformat()]


def test_mark_missing_habit_done_shows_error(client):
    response = client.post('/habits/9999/done', follow_redirects=True)
    assert response.status_code == 200
    assert b'Habit not found' in response.data


def test_mark_invalid_habit_id_done_shows_error(client):
    response = client.post('/habits/invalid/done', follow_redirects=True)
    assert response.status_code == 200
    assert b'Habit not found' in response.data


# Delete habit tests
def test_delete_habit_removes_it_from_dashboard(client):
    create_habit(client, name='Hydrate', description='Drink water')
    data = load_data()
    habit_id = data['habits'][0]['id']

    response = client.post(f'/habits/{habit_id}/delete', follow_redirects=True)
    assert response.status_code == 200
    assert b'Habit deleted successfully' in response.data
    assert b'Hydrate' not in response.data

    data = load_data()
    assert data['habits'] == []


def test_delete_missing_habit_shows_error(client):
    response = client.post('/habits/9999/delete', follow_redirects=True)
    assert response.status_code == 200
    assert b'Habit not found' in response.data


def test_delete_invalid_habit_id_shows_error(client):
    response = client.post('/habits/invalid/delete', follow_redirects=True)
    assert response.status_code == 200
    assert b'Habit not found' in response.data


# Data persistence tests
def test_habit_data_persists_after_edit(client):
    create_habit(client, name='Read', description='Read books')
    data = load_data()
    habit_id = data['habits'][0]['id']

    client.post(
        f'/habits/{habit_id}/edit',
        data={'name': 'Study', 'description': 'Study code'},
        follow_redirects=True,
    )

    data = load_data()
    assert data['habits'][0]['name'] == 'Study'
    assert data['habits'][0]['description'] == 'Study code'
    assert data['habits'][0]['id'] == habit_id


def test_completion_dates_persist_after_delete(client):
    create_habit(client, name='Exercise')
    data = load_data()
    habit_id = data['habits'][0]['id']

    client.post(f'/habits/{habit_id}/done', follow_redirects=True)
    data = load_data()
    assert data['habits'][0]['completion_dates'] == [date.today().isoformat()]

    client.post(f'/habits/{habit_id}/delete', follow_redirects=True)
    data = load_data()
    assert data['habits'] == []


def test_multiple_habits_maintain_separate_completions(client):
    create_habit(client, name='Habit1')
    create_habit(client, name='Habit2')
    data = load_data()
    id1, id2 = data['habits'][0]['id'], data['habits'][1]['id']

    client.post(f'/habits/{id1}/done', follow_redirects=True)
    data = load_data()

    assert data['habits'][0]['completion_dates'] == [date.today().isoformat()]
    assert data['habits'][1]['completion_dates'] == []
