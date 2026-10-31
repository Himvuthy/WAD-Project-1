# Lab 04: Forms, Validation, and Session State

## Project Theme

EduRisk Analytics

## Description

This Streamlit app is a student academic monitoring prototype. It continues
from Lab 03 and improves the Risk Checker using forms, input validation, and
session state. Student data loads from `students.csv` using Pandas.

## Features

- Sidebar navigation
- Home, Dashboard, Student Data, Risk Checker, and About pages
- CSV data loading and a clear error when `students.csv` is missing
- Dashboard metrics, filters, charts, and filtered CSV downloads
- Risk calculation based on score and attendance
- Risk Checker form with a Check Risk submit button
- Empty and whitespace-only student name validation
- Score and attendance inputs limited to 0–100
- Supportive feedback for Low, Medium, and High Risk
- Temporary session history displayed in Recent Risk Checks
- Clear History button that immediately empties the table
- Ethics reminders for responsible academic support

Risk history lasts for the current Streamlit session. It is not saved to
`students.csv`. A score or attendance below 60 means High Risk; otherwise, a
value below 75 means Medium Risk. All other cases are Low Risk.

## Tools Used

- Python
- Streamlit
- Pandas
- VS Code

## How to Run

From the folder containing `app.py`, using your existing virtual environment:

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Required Files

- `app.py`
- `students.csv`
- `requirements.txt`
- `README.md`

## Lab 04 Checks

Submit an empty or whitespace-only name: a warning appears and history stays
unchanged. Submit Student A (90, 95), Student B (70, 80), Student C (50, 85),
and Student D (80, 55): the results should be Low, Medium, High, and High Risk.
Visit another page and return to confirm history remains. Clear History should
show both the confirmation and “No risk checks yet.”

## Submission

Include only the four required files in `studentid_name_lab04.zip`, replacing
the placeholders with your information. Exclude `.venv/`, `__pycache__/`, and
downloaded `filtered_student_data.csv` files.

## Student Information

Name:
Student ID:
Class:
