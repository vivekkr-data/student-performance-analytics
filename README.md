# Student Performance Analytics System

Python with AI mini project | Vivek Kumar | 24BCE2234

**Status: application executed successfully on the supplied Kaggle CSV; 30 records analyzed, 27 automated tests passed.**

Repository: https://github.com/vivekkr-data/student-performance-analytics

[Project documentation (PDF)](documentation/Project_Documentation.pdf) | [Full analysis](outputs/performance_summary.txt) | [Student results](outputs/student_results.csv)

## Overview and objective
Read a student CSV, validate its contents, and produce clear student, subject, class, department and attendance summaries. The project demonstrates Python functions, loops and conditions, NumPy numerical operations and Pandas data analysis. No machine-learning model or web application is used.

## Technologies and requirements
Python 3.11+ (tested with Python 3.12.14), NumPy 2.3.5 and Pandas 2.2.3. CSV stores inputs and exports. Git/GitHub are used for publication once the target repository is available. PDF documentation is pre-generated and needs no extra runtime dependencies.

## Dataset and provenance
Source: [TSS Pandas Challenge #1](https://www.kaggle.com/competitions/tss-pandas-challenge-1/data), hosted by Gagan H.

The user supplied the downloaded Kaggle archive `tss-pandas-challenge-1.zip`. Its actual student file is `student_data.csv` (underscore), although the source page describes a hyphenated filename. It is included here byte-for-byte as `students.csv`: **30 rows and 9 columns**, with no missing values or duplicate student IDs. The archive's competition answer template is not needed for this assignment and is excluded.

Both selected subject scores are treated as marks out of 100 under the project's declared grading model. All observed marks are within that range; the source CSV does not itself encode a maximum-score field. The dataset was designed for Pandas practice and is not represented as independently collected student observations. No independent redistribution license was found in the supplied archive or retrievable source page; no license over the source data is asserted by this project. See `DATASET_SOURCE.md` for the byte checksum and attribution.

| Column | Meaning |
|---|---|
| student_id | Unique student identifier, preserved as text |
| name | Student name |
| department | Department |
| year | Year of study; retained as source metadata |
| age | Age; retained as source metadata |
| attendance | Percentage, 0 to 100 |
| python_marks | Python score, assumed out of 100 |
| ml_marks | ML score, assumed out of 100 |
| projects_completed | Source metadata; excluded from exam marks |

At least 20 records are required by this implementation. The assignment permits 15-20 or more. Additional metadata is retained; missing optional metadata is displayed, not used in score calculations. Required analytical fields cannot be missing. Validation rejects duplicate IDs, blank required text, surrounding text whitespace, duplicate headers, nonnumeric or nonfinite scores, out-of-range attendance/marks, and reserved output column names. It does not silently clean or discard rows.

## Setup and run
From the project directory:

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Linux/macOS:

```bash
source .venv/bin/activate
```

Then:

```bash
python -m pip install -r requirements.txt
python main.py
python -m unittest discover -s tests -v
```

Alternative paths:

```bash
python main.py --data /path/to/students.csv --output /path/to/reports
```

Alternative verified subjects, each out of 100:

```bash
python main.py --subjects math_marks science_marks
```

The alternate CSV must still include `student_id`, `name`, `department` and `attendance`. Explicitly adapt the original dataset if necessary and document the transformation; never invent missing identifiers or departments while claiming they are original data. Default file paths resolve relative to `main.py`, allowing execution from another directory.

## Formulas and project assumptions
For m subjects, each out of 100:

- Total = sum of subject scores.
- Average = total / m.
- Percentage = total / (100 x m) x 100.
- PASS requires every subject score >= 40. Otherwise FAIL and grade F.
- Pass percentage = passed / student count x 100.
- Population standard deviation uses `ddof=0`.

| Percentage (all subjects passed) | Grade |
|---|---|
| 90 to 100 | A+ |
| 80 to below 90 | A |
| 70 to below 80 | B |
| 60 to below 70 | C |
| 50 to below 60 | D |
| 40 to below 50 | E |
| Below 40, or any failed subject | F |

These are project rules, not institutional regulations. Calculations and grade decisions use unrounded values. Console tables show two decimals; CSV exports use up to ten significant digits. Attendance below 75% is flagged without changing exam pass/fail status.

## Features and analysis
- Pandas CSV loading, first five rows, dimensions, column names, `info()`, missing counts and `describe()`.
- NumPy row totals/means, class statistics and population standard deviation.
- Per-student total, average, percentage, grade and status.
- Passed/failed counts and percentages, grade distribution.
- Highest and lowest totals/averages, mean, median and all tied highest/lowest students.
- Subject mean, maximum, minimum, median, deviation and pass rates.
- Top five rows sorted by average descending, total descending, then student ID lexicographically ascending. Tied scores share competition rank; exactly five rows are shown, so a boundary tie may be split using ID order.
- Department counts, means and pass rates using `groupby()`; tied extremes retained.
- Attendance summary, below-75% list and Pearson correlation when defined.
- Clear data-supported summary; no causal claims.

## Project structure
```text
students.csv                Original supplied CSV, renamed without changes
main.py                     Console entry point and error handling
functions.py                Validation, calculations, reporting, exports
requirements.txt            Exact tested dependencies
README.md                   Setup, rules and submission status
DATASET_SOURCE.md           Authentic-data acquisition and permission status
.gitignore                  Cache, environment and credential exclusions
tests/test_functions.py     Synthetic-only automated tests
documentation/
  Project_Documentation.md  Required ten sections with verified results
  Project_Documentation.pdf Formatted PDF of the completed analysis
  REQUIREMENTS_CHECKLIST.md Requirement-to-code mapping and submission checklist
  evidence/                 Actual execution logs, not screenshots
```
The verified run generated `outputs/`, containing `student_results.csv`, `subject_analysis.csv`, `department_analysis.csv` and `performance_summary.txt`. The first preserves source columns plus computed results. The text report contains the full console analysis. Existing files at the chosen output location are overwritten on subsequent runs; choose a new output directory to retain earlier reports.

## Verified results
| Metric | Result |
|---|---:|
| Students analyzed | 30 |
| Passed / failed | 30 / 0 |
| Pass percentage | 100.00% |
| Class average | 82.35 / 100 |
| Highest performer | Sanya, ID 22: 97.50 / 100 |
| Lowest performer | Manish, ID 21: 63.00 / 100 |
| Python average | 81.40 / 100 |
| ML average | 83.30 / 100 |
| Average attendance | 82.60% |
| Students below 75% attendance | 7 (23.33%) |

All 30 students passed under the declared subject threshold; this does not imply that the application cannot detect failures. Synthetic tests exercise failure cases, including failure in one subject despite a high average.

## Testing and execution evidence
```bash
python -m unittest discover -s tests -v
python main.py
```

27 automated tests passed. They cover validation, boundaries, ties, numerical calculations, exports and execution from a different working directory. Controlled synthetic fixtures are used only inside tests. Separately, the supplied Kaggle CSV was processed by the real application with exit code 0. Python's standard `csv` and `statistics` modules independently checked every student's total/average and the important class aggregates against exported results.

Evidence:
- `documentation/evidence/actual_run.txt`: genuine full program output.
- `documentation/evidence/test_run.txt`: genuine test-run log.
- `documentation/evidence/independent_verification.json`: independently calculated aggregate results.

No terminal screenshot images are fabricated. The report includes actual output excerpts, and the full text logs are available for inspection.

## GitHub and submission
Repository: https://github.com/vivekkr-data/student-performance-analytics

Clone and run:
```bash
git clone https://github.com/vivekkr-data/student-performance-analytics.git
cd student-performance-analytics
python -m pip install -r requirements.txt
python main.py
```

Deadline in the supplied assignment: **15 October 2026**. Paste the repository URL into the EWB Google Form and submit it. The Google Form URL was not supplied, and form submission has not been performed.

## Learning outcomes and limitations
The implementation demonstrates validation, NumPy array calculations, Pandas grouping/filtering/sorting, reusable functions, testing and reproducible execution. Study each function before evaluation.

Every selected subject must use the declared 100-point scale. Grades and the 75% attendance flag are project assumptions, not official institutional rules. Invalid required data is rejected rather than silently repaired. Correlation is descriptive and does not establish causation. The small practice dataset limits generalization. Console values are rounded for readability; decisions use unrounded values.

Author: **Vivek Kumar - 24BCE2234**.
