# Student Performance Analytics System

**A Python console application that turns student marks and attendance into clear academic reports.**

Built for the **Python with AI** mini project using Python, NumPy and Pandas.

**Author:** Vivek Kumar · **Registration:** 24BCE2234

[Project report (PDF)](documentation/Project_Documentation.pdf) · [Student results](outputs/student_results.csv) · [Full analysis](outputs/performance_summary.txt) · [Test evidence](documentation/evidence/test_run.txt)

## At a glance

| Dataset | Class average | Pass rate | Verification |
|---|---|---|---|
| 30 students · 2 subjects · 4 departments | **82.35 / 100** | **100%** (30 passed, 0 failed) | **31 automated tests passed** |

The application loads `students.csv`, validates the data, calculates each student's performance, prints the analysis, and saves four reports. The original dataset is included, so no Kaggle login is needed to run this repository.

## Quick start

### 1. Download the project

Use **Code → Download ZIP** on GitHub and extract it, or clone it:

```bash
git clone https://github.com/vivekkr-data/student-performance-analytics.git
cd student-performance-analytics
```

If you downloaded the ZIP, open a terminal inside the extracted folder containing `main.py`.

### 2. Run the project

Use Python 3.11 or 3.12. Tested with Python 3.12.14, NumPy 2.3.5 and Pandas 2.2.3.

```bash
python -m pip install -r requirements.txt
python main.py
```

No API keys, database, web server or machine-learning packages are required.

### 3. Open the results

The console prints the full analysis. Reports are written to [`outputs/`](outputs/):

| File | Contents |
|---|---|
| [student_results.csv](outputs/student_results.csv) | All original columns plus total, average, percentage, grade and status |
| [subject_analysis.csv](outputs/subject_analysis.csv) | Mean, highest, lowest, median, population deviation and pass rate per subject |
| [department_analysis.csv](outputs/department_analysis.csv) | Student count, mean score, pass count and pass rate per department |
| [performance_summary.txt](outputs/performance_summary.txt) | Full readable report, including dataset overview and final insights |

Running again replaces these four files in the selected output folder. Use `--output` to preserve a separate run.

## What the application does

| Stage | Analysis |
|---|---|
| Inspect | First five rows, dimensions, column names, data types, missing values and descriptive statistics |
| Calculate | Student-wise totals, averages, percentages, grades and pass/fail |
| Summarize | Class mean, median, population deviation, highest/lowest scores, pass/fail totals and grade distribution |
| Compare subjects | Python and ML statistics, strongest/weakest subject and difference in means |
| Rank | Top five students; every tied highest/lowest student is included in the summary |
| Group | Department-wise counts, means and pass rates using Pandas `groupby()` |
| Check attendance | Mean, maximum, minimum, students below 75%, and correlation with average marks |
| Export | Three CSV reports and one text report |

## Verified results

The following values come from executing the included CSV, not sample output.

| Metric | Result |
|---|---:|
| Student count | 30 |
| Passed / failed | 30 / 0 |
| Pass percentage | 100.00% |
| Class average | 82.35 / 100 |
| Class median | 84.00 / 100 |
| Class population standard deviation | 9.65 marks |
| Highest performer | Sanya (ID 22): 195 / 200, average 97.50 |
| Lowest performer | Manish (ID 21): 126 / 200, average 63.00 |
| Python mean | 81.40 / 100 |
| ML mean | 83.30 / 100 |
| Average attendance | 82.60% |
| Attendance below 75% | 7 students (23.33%) |

### Top five students

| Rank | ID | Name | Department | Total / 200 | Average / 100 | Grade |
|---:|---:|---|---|---:|---:|---|
| 1 | 22 | Sanya | AIML | 195 | 97.50 | A+ |
| 2 | 29 | Nikhil | AIML | 193 | 96.50 | A+ |
| 3 | 11 | Rahul | AIML | 189 | 94.50 | A+ |
| 3 | 19 | Varun | CSE | 189 | 94.50 | A+ |
| 5 | 2 | Ananya | AIML | 185 | 92.50 | A+ |

Sorting uses average descending, total descending, then student ID **as text** ascending. Equal scores share competition rank (1, 2, 3, 3, 5). The display contains exactly five rows; ties at the fifth position are resolved by ID order. All tied class highest/lowest students are still included in the final summary.

All supplied students meet the pass rule. Separate tests verify that failing records are correctly identified.

## Calculations and grading

For two equally weighted subjects, each treated as out of 100:

```text
Total marks = Python marks + ML marks
Average marks = Total marks / 2
Percentage = Total marks / 200 × 100
Pass percentage = Passed students / Total students × 100
```

A student passes only when **every subject score is at least 40**. Failure in any subject gives overall **FAIL** and grade **F**, regardless of the average.

| Percentage, with every subject passed | Grade |
|---|---|
| 90–100 | A+ |
| 80–below 90 | A |
| 70–below 80 | B |
| 60–below 70 | C |
| 50–below 60 | D |
| 40–below 50 | E |
| Below 40, or a failed subject | F |

For example, Python = 39 and ML = 100 gives total = 139 and average = 69.50, but the final status is **FAIL**, grade **F**.

- Grades use unrounded values; console tables display two decimals.
- CSV numbers use up to ten significant digits.
- Population standard deviation uses `ddof=0`.
- Attendance below 75% is a separate observation, not an exam-failure rule.
- Grades, equal subject weights and the attendance threshold are **project assumptions**, not institutional regulations.
- Correlation is descriptive, not evidence that attendance causes a score change. A constant input makes correlation undefined (`None`).

## Dataset

Source: [TSS Pandas Challenge #1 — Kaggle](https://www.kaggle.com/competitions/tss-pandas-challenge-1/data), hosted by Gagan H.

The supplied archive contains `student_data.csv`. Its bytes are preserved unchanged as [`students.csv`](students.csv): **30 rows, 9 columns**, zero missing values and unique IDs. The competition answer template is not used in this project.

| Column | Role |
|---|---|
| `student_id` | Unique ID, stored as text to preserve leading zeroes |
| `name` | Student name |
| `department` | Department grouping |
| `year` | Original metadata; excluded from marks |
| `age` | Original metadata; excluded from marks |
| `attendance` | Attendance percentage, 0–100 |
| `python_marks` | Python exam score |
| `ml_marks` | ML exam score |
| `projects_completed` | Original metadata; excluded from marks |

The dataset is intended for Pandas practice. The CSV does not encode maximum-score fields; the analysis explicitly assumes both subjects are out of 100. See [dataset provenance](DATASET_SOURCE.md) for the exact checksum, source attribution and license status. No independent open-data license is asserted here.

## Validation and error handling

The program rejects:

- Fewer than 20 student records or missing required columns.
- Empty files, blank/duplicate headers, malformed quoting, and rows with missing/extra fields.
- Missing or blank student details, duplicate IDs and surrounding whitespace in identity fields.
- Missing, nonnumeric, infinite or out-of-range marks/attendance.
- Output columns already present in the input, to prevent overwriting original data.
- Identity fields, age, year, attendance or project count selected as exam subjects.

It does not fill invalid scores with zero, silently drop rows, or rewrite the input CSV. Optional source metadata is preserved. Ordinary input/file errors produce a readable message and exit code 1; successful runs exit with 0.

## Tests and evidence

Run tests from the project folder:

```bash
python -m unittest discover -s tests -v
```

**31 tests passed.** Coverage includes calculations, grade boundaries, subject failure, tied ranks, department/attendance analysis, CSV structure, quoted names, leading-zero IDs, invalid inputs, exports, CLI execution and the bundled dataset's reference results. Tests use temporary directories for exports.

The supplied CSV was also run end to end. Standard-library `csv` and `statistics` calculations independently checked all student totals/averages, subject means/deviations and department counts/means.

| Evidence | Purpose |
|---|---|
| [Actual run](documentation/evidence/actual_run.txt) | Genuine program output |
| [Test run](documentation/evidence/test_run.txt) | Executed test names and results |
| [Independent verification](documentation/evidence/independent_verification.json) | Separately calculated reference values |

The report includes genuine text output. Screenshot images are optional in the assignment and are not included.

## Code guide

| File / functions | Responsibility |
|---|---|
| [`main.py`](main.py) | Parse options, load/validate, call analysis, export and print |
| `load_student_data`, `validate_student_data` | Read CSV and check its structure/content |
| `calculate_student_results`, `assign_grade`, `determine_pass_status` | Compute individual results |
| `calculate_class_statistics`, `analyze_subjects` | Class and subject statistics |
| `analyze_departments`, `analyze_attendance` | Grouping and attendance analysis |
| `get_top_performers` | Deterministic ranking |
| `build_report`, `display_summary`, `export_results` | Presentation and output files |

Calculation functions are in [`functions.py`](functions.py). Python loops and conditions implement grading and report construction; NumPy handles numerical arrays; Pandas handles DataFrames, filtering, grouping, sorting and CSV I/O.

## Optional commands

```bash
python main.py --help
python main.py --output reports_second_run
python main.py --data "path/to/another_students.csv" --output reports_custom
```

For a separate CSV with different exam columns, each out of 100:

```bash
python main.py --data "path/to/another_students.csv" --subjects math_marks science_marks
```

That file must still contain `student_id`, `name`, `department` and `attendance`. Default paths are relative to `main.py`; explicitly supplied relative paths are relative to your terminal's current folder.

## Documentation and submission

The [PDF report](documentation/Project_Documentation.pdf) and [Markdown report](documentation/Project_Documentation.md) contain the assignment's ten sections in order: Project Title, Objective, Technologies Used, Dataset Description, Implementation, Key Features, Output, Final Outcome, Challenges & Learning, and GitHub Repository.

[Requirement checklist](documentation/REQUIREMENTS_CHECKLIST.md) maps the brief to the implementation.

**Deadline:** 15 October 2026. Submit this repository link in the EWB Google Form:

https://github.com/vivekkr-data/student-performance-analytics

Google Form submission has not been performed. The project uses a small practice dataset; results should not be generalized to a larger student population.
