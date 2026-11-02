# Truck Finance Tracker

A Python desktop application for recording truck income, operating expenses, and maintenance. Built with Tkinter, pandas, and python-dateutil, with a Greek-language interface.

## Features

- Add entries with date, type, category, amount, and description.
- Track income, expenses, and maintenance separately.
- Filter the records table by entry type.
- Generate financial summaries for a selected starting month and duration.
- Calculate income, recorded expenses including maintenance, maintenance count, and the difference between income and expenses.
- Store records locally in a CSV file.

## Requirements

- Python 3 with Tkinter installed and a graphical desktop environment.
- pandas and python-dateutil (see requirements.txt).

Tkinter is included with many Python distributions. If unavailable, install the Tkinter package appropriate for your operating system.

## Installation

```bash
git clone https://github.com/narbanite/truck-finance-tracker.git
cd truck-finance-tracker
python -m venv .venv
```

Activate the environment:

```bash
# Windows PowerShell
.venv\Scripts\Activate.ps1

# macOS / Linux
source .venv/bin/activate
```

Install dependencies and launch from the repository directory:

```bash
python -m pip install -r requirements.txt
python truck.py
```

## Usage

1. Enter a date in YYYY-MM-DD format.
2. Select income, expense, or service.
3. Enter a category, amount, and optional description, then add the entry.
4. Use the table filter to display a specific entry type.
5. Select a month, year, duration, and optional entry-type filter to display a summary. Choose Όλα for a complete income-and-expenses summary.

## Data and privacy

The application reads and writes truck_data.csv in the current working directory. If the file does not exist, the application starts with an empty table and creates it when an entry is saved. Run the application from the repository directory for a consistent data location.

Existing user records are not included in this repository. The data file is excluded through .gitignore. Data is stored as an unencrypted local CSV; keep backups and avoid sharing sensitive records.

CSV columns: date, type, category, amount, description.

## Status and known limitations

This repository preserves the original application code. A Python syntax check was completed before upload; GUI behaviour and end-to-end functionality have not been verified in the publishing environment.

- The summary control is labelled Μήνες πίσω (months back), but the current calculation starts at the selected month and extends forward by the selected duration. The upper boundary is exclusive.
- Date input is not validated on entry. Invalid dates may cause summary calculation errors.
- Blank amounts are stored as zero; stricter amount validation is not implemented.
- Editing and deleting records are not implemented.
- This is a simple record-keeping project, not a full accounting or tax application.

## Author

Nikoletta Arvaniti
