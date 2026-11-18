# Habit Tracker Pro

Habit Tracker Pro is a simple local Flask web application for tracking daily habits, measuring current streaks, and viewing weekly completion analytics. The app stores habit data in a local JSON file and uses a minimal web interface without external APIs or third-party front-end dependencies.

## Features

- Create, view, edit, and delete habits
- Mark habits as complete for the current day
- Prevent duplicate completions for the same habit on the same date
- Track the current streak for each habit
- Display weekly completion analytics
- Store data locally in `data/habits.json`
- Show success and error feedback using flash messages

## Non-Trivial Logic Feature: Current Streak Engine

The main non-trivial logic feature is the current streak engine. It calculates each habit's current streak by evaluating completion dates and counting backwards from today or yesterday.

The streak engine handles:

- Empty completion history
- Duplicate completion dates
- Out-of-order completion entries
- Invalid date strings
- Missed days that reset the current streak
- Month and year boundaries

## Technologies Used

- Python 3
- Flask
- Jinja2 templates
- HTML/CSS/JavaScript
- pytest

## Project Structure

```text
habit-tracker-pro/
├── app.py
├── requirements.txt
├── data/
│   └── habits.json
├── services/
├── storage/
├── templates/
├── static/
└── tests/

## Installation

1. Clone the repository or download the project files.

2. Open a terminal in the project root folder.

3. Create a Python virtual environment:

```bash
python -m venv venv
```

4. Activate the virtual environment.

On Windows:

```bash
venv\Scripts\activate
```

On macOS/Linux:

```bash
source venv/bin/activate
```

5. Install dependencies from `requirements.txt`:

```bash
pip install -r requirements.txt
```

## Run the App Locally

From the project root folder, run:

```bash
python app.py
```

Then open the following address in your browser:

```text
http://127.0.0.1:5000
```

The application will run locally on your machine.

## Run Tests

From the project root folder, run:

```bash
python -m pytest
```

The test suite includes unit tests for the streak engine, date handling, JSON storage, and analytics service, as well as integration tests for the Flask routes.

## Data Storage

Habit data is stored locally in:

```text
data/habits.json
```

If the file does not exist, the application creates an empty data file automatically.

## Notes

- No external APIs are used.
- No cloud storage is used.
- No user accounts or login are required.
- Static assets are served locally.
- No external CDNs or front-end JavaScript libraries are required.