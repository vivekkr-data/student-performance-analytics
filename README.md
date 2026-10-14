# Student Performance Analytics System

Python with AI mini project by Vivek Kumar (24BCE2234).

## Status
The Python application and 27 automated tests are complete. Source code is published here. The supplied dataset and reports remain in the local delivery package pending explicit approval to publish student-level names, marks and attendance. They are not included in this repository yet.

## Features
Student totals, averages, grades and pass/fail; class and subject statistics; top performers; department and attendance analysis; validation; CSV and text exports.

## Setup
Requires Python 3.11+; tested on Python 3.12.14.

```bash
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
```

To run analysis, place the original supplied CSV next to main.py as students.csv, then run:

```bash
python main.py
```

The dataset requires student_id, name, department, attendance, python_marks and ml_marks columns, and at least 20 valid records. See DATASET_SOURCE.md for attribution. Do not commit credentials.

## Calculation rules
Each selected subject is treated as out of 100. Total is the sum; average is total divided by subject count; percentage is total divided by maximum total times 100. PASS requires at least 40 in every subject. Any subject failure gives grade F; otherwise grade thresholds 90/80/70/60/50/40 give A+/A/B/C/D/E. These are project assumptions. Attendance below 75% is a separate observation.

## Tests
27 tests passed with synthetic fixtures, including grade boundaries, failure cases, tied ranks, validation, exports and command-line execution. The application was also executed successfully on the supplied CSV; its reports await publication approval.

## Submission
The project repository URL must be submitted through the EWB Google Form after the remaining project files are published. Form submission has not been performed.
