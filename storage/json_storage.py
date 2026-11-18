# storage/json_storage.py
# Handles storage of habit data in JSON format.

import json
import os
import tempfile

DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'habits.json')


def _ensure_storage_file():
    os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
    if not os.path.exists(DATA_PATH) or os.path.getsize(DATA_PATH) == 0:
        with open(DATA_PATH, 'w', encoding='utf-8') as storage_file:
            json.dump({'habits': []}, storage_file, indent=2)


def load_data():
    """Load habit data from the local JSON storage file."""
    _ensure_storage_file()

    try:
        with open(DATA_PATH, 'r', encoding='utf-8') as storage_file:
            content = storage_file.read()
            if not content.strip():
                return {'habits': []}
            data = json.loads(content)
            if isinstance(data, dict):
                return data
    except (OSError, json.JSONDecodeError):
        pass

    return {'habits': []}


def save_data(data):
    """Save habit data safely to the local JSON storage file."""
    os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)

    dir_name = os.path.dirname(DATA_PATH)
    with tempfile.NamedTemporaryFile('w', encoding='utf-8', dir=dir_name, delete=False) as temp_file:
        json.dump(data, temp_file, indent=2)
        temp_file.flush()
        os.fsync(temp_file.fileno())
        temp_name = temp_file.name

    os.replace(temp_name, DATA_PATH)


class JSONStorage:
    def __init__(self, file_path=DATA_PATH):
        self.file_path = file_path

    def read(self):
        return load_data()

    def write(self, data):
        save_data(data)
