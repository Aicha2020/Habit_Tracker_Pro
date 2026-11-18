# tests/test_json_storage.py
# Tests for JSON storage layer functionality.

import json
import os

import pytest

import storage.json_storage as json_storage
from storage.json_storage import load_data, save_data


@pytest.fixture
def temp_storage(tmp_path, monkeypatch):
    """Fixture to use a temporary JSON file for storage."""
    temp_file = tmp_path / 'test_habits.json'
    monkeypatch.setattr(json_storage, 'DATA_PATH', str(temp_file))
    yield temp_file
    # Cleanup
    if temp_file.exists():
        temp_file.unlink()


# File creation tests
def test_load_data_creates_file_if_not_exists(temp_storage):
    """load_data() should create the JSON file if it does not exist."""
    assert not temp_storage.exists()

    data = load_data()

    assert temp_storage.exists()
    assert data == {'habits': []}


def test_load_data_initializes_with_empty_habits(temp_storage):
    """load_data() should return {'habits': []} for a new file."""
    data = load_data()
    assert data == {'habits': []}
    assert isinstance(data['habits'], list)


def test_load_data_handles_empty_file(temp_storage):
    """load_data() should handle an empty JSON file gracefully."""
    temp_storage.write_text('')

    data = load_data()
    assert data == {'habits': []}


def test_load_data_handles_invalid_json(temp_storage):
    """load_data() should handle invalid JSON gracefully."""
    temp_storage.write_text('{ invalid json }')

    data = load_data()
    assert data == {'habits': []}


def test_load_data_handles_corrupted_structure(temp_storage):
    """load_data() should handle JSON that is not a dict gracefully."""
    temp_storage.write_text('[1, 2, 3]')

    data = load_data()
    assert data == {'habits': []}


# Save and persistence tests
def test_save_data_persists_to_file(temp_storage):
    """save_data() should persist data to the JSON file."""
    test_data = {
        'habits': [
            {'id': 1, 'name': 'Exercise', 'description': 'Workout', 'completion_dates': []}
        ]
    }

    save_data(test_data)

    with open(temp_storage, 'r') as f:
        persisted = json.load(f)

    assert persisted == test_data


def test_save_data_preserves_completion_dates(temp_storage):
    """save_data() should correctly preserve completion_dates."""
    test_data = {
        'habits': [
            {
                'id': 1,
                'name': 'Read',
                'description': 'Read books',
                'created_at': '2026-05-01',
                'completion_dates': ['2026-05-10', '2026-05-11', '2026-05-12']
            }
        ]
    }

    save_data(test_data)
    loaded = load_data()

    assert loaded['habits'][0]['completion_dates'] == ['2026-05-10', '2026-05-11', '2026-05-12']


def test_save_and_load_roundtrip(temp_storage):
    """Data saved and loaded should match original data."""
    original = {
        'habits': [
            {
                'id': 1,
                'name': 'Meditate',
                'description': 'Morning meditation',
                'created_at': '2026-05-01',
                'completion_dates': ['2026-05-15']
            },
            {
                'id': 2,
                'name': 'Exercise',
                'description': 'Evening workout',
                'created_at': '2026-05-02',
                'completion_dates': ['2026-05-14', '2026-05-15']
            }
        ]
    }

    save_data(original)
    loaded = load_data()

    assert loaded == original


# Overwrite and update tests
def test_save_data_overwrites_previous_data(temp_storage):
    """save_data() should overwrite previous data."""
    data1 = {'habits': [{'id': 1, 'name': 'Habit1', 'completion_dates': []}]}
    data2 = {'habits': [{'id': 2, 'name': 'Habit2', 'completion_dates': []}]}

    save_data(data1)
    save_data(data2)

    loaded = load_data()
    assert loaded == data2
    assert len(loaded['habits']) == 1
    assert loaded['habits'][0]['id'] == 2


def test_multiple_save_load_cycles_maintain_data(temp_storage):
    """Multiple save/load cycles should maintain data integrity."""
    for i in range(3):
        data = {
            'habits': [
                {'id': i, 'name': f'Habit{i}', 'completion_dates': [f'2026-05-{10+i}']}
            ]
        }
        save_data(data)
        loaded = load_data()
        assert loaded == data


# Edge cases
def test_save_data_with_empty_habits_list(temp_storage):
    """save_data() should handle empty habits list."""
    data = {'habits': []}
    save_data(data)
    loaded = load_data()
    assert loaded == {'habits': []}


def test_save_data_with_special_characters(temp_storage):
    """save_data() should handle special characters in habit names."""
    data = {
        'habits': [
            {
                'id': 1,
                'name': 'Exercise & Meditate',
                'description': 'Do "stretches" today',
                'completion_dates': []
            }
        ]
    }
    save_data(data)
    loaded = load_data()
    assert loaded['habits'][0]['name'] == 'Exercise & Meditate'
    assert loaded['habits'][0]['description'] == 'Do "stretches" today'


def test_json_file_is_properly_formatted(temp_storage):
    """Saved JSON file should be properly formatted with indentation."""
    data = {'habits': [{'id': 1, 'name': 'Test', 'completion_dates': []}]}
    save_data(data)

    content = temp_storage.read_text()
    assert '  ' in content  # Should have indentation
