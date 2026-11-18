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

## Logic Feature: Current Streak Engine

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

## AI-Assisted Development

Habit Tracker Pro was developed with assistance from Google Gemini and GitHub Copilot. Gemini supported planning, requirements analysis, and system design, while GitHub Copilot assisted with implementation, debugging, and testing. AI-generated outputs were manually reviewed and validated against the project requirements, with final decisions remaining the responsibility of the developer.

## Project Structure

```text
habit-tracker-pro/
├── app.py
├── README.md
├── requirements.txt
├── data/
│   └── habits.json
├── services/
│   ├── habit_service.py
│   ├── streak_engine.py
│   └── analytics_service.py
├── storage/
│   └── json_storage.py
├── templates/
├── static/
└── tests/
```

## Installation

1. Clone the repository or download the project files.

2. Open a terminal in the project root folder.

3. Create a Python virtual environment:

```bash
python -m venv venv
```

4. Activate the virtual environment.

On Windows:

```powershell
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

`http://127.0.0.1