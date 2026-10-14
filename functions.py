"""Validated student analytics using NumPy and Pandas."""

from pathlib import Path
import csv
import io
import numpy as np
import pandas as pd

SUBJECTS = ("python_marks", "ml_marks")
GRADES = ("A+", "A", "B", "C", "D", "E", "F")


def load_student_data(path):
    """Read CSV without losing leading zeroes in student IDs."""
    path = Path(path)
    if not path.is_file():
        raise ValueError(
            f"Dataset not found: {path}. Place student_data.csv from the Kaggle archive here as students.csv."
        )
    try:
        with path.open(encoding="utf-8-sig", newline="") as stream:
            reader = csv.reader(stream, strict=True)
            header = next(reader, [])
            if not header:
                raise ValueError("The CSV is empty.")
            if any(not column.strip() for column in header):
                raise ValueError("CSV column names cannot be blank.")
            if len(header) != len(set(header)):
                raise ValueError("Duplicate CSV column names are not allowed.")
            for row in reader:
                if len(row) != len(header):
                    raise ValueError(
                        f"CSV line {reader.line_num}: expected {len(header)} fields, "
                        f"found {len(row)}. Check missing or extra commas."
                    )
        return pd.read_csv(
            path,
            dtype={"student_id": "string"},
            encoding="utf-8-sig",
            skip_blank_lines=False,
        )
    except (
        csv.Error,
        pd.errors.EmptyDataError,
        pd.errors.ParserError,
        UnicodeError,
    ) as error:
        raise ValueError(f"Cannot read CSV: {error}") from error


def validate_student_data(data, subjects=SUBJECTS, minimum_records=20):
    """Reject invalid required data; never fill scores or discard rows."""
    subjects = tuple(subjects)
    if not subjects or len(subjects) != len(set(subjects)):
        raise ValueError("Choose one or more unique subject columns.")
    if set(subjects) & {
        "student_id",
        "name",
        "department",
        "attendance",
        "year",
        "age",
        "projects_completed",
    }:
        raise ValueError(
            "Student details, attendance and project counts cannot be exam subjects."
        )
    required = ["student_id", "name", "department", "attendance", *subjects]
    missing = sorted(set(required) - set(data.columns))
    if missing:
        raise ValueError("Missing columns: " + ", ".join(missing))
    if not data.columns.is_unique:
        raise ValueError("Duplicate column names are not allowed.")
    if len(data) < minimum_records:
        raise ValueError(
            f"At least {minimum_records} records required; found {len(data)}."
        )
    reserved = {"total_marks", "average_marks", "percentage", "grade", "status", "rank"}
    if reserved & set(data.columns):
        raise ValueError(
            "Input contains reserved result columns: "
            + ", ".join(sorted(reserved & set(data.columns)))
        )
    result = data.copy(deep=True)
    for column in ["student_id", "name", "department"]:
        values = result[column].astype("string")
        if values.isna().any() or values.str.strip().eq("").any():
            raise ValueError(f"{column}: missing or blank values.")
        if values.ne(values.str.strip()).any():
            raise ValueError(
                f"{column}: remove surrounding whitespace explicitly in the source."
            )
        result[column] = values
    if result["student_id"].duplicated().any():
        raise ValueError("Duplicate student IDs are not allowed.")
    for column in ["attendance", *subjects]:
        values = pd.to_numeric(result[column], errors="coerce")
        if values.isna().any() or not np.isfinite(values.to_numpy(dtype=float)).all():
            raise ValueError(
                f"{column}: all values must be finite numbers, with no missing values."
            )
        if not values.between(0, 100).all():
            raise ValueError(f"{column}: values must be between 0 and 100.")
        result[column] = values
    return result


def assign_grade(percentage, passed=True):
    """Project grading policy: failure in any subject overrides average grade."""
    if not np.isfinite(percentage) or not 0 <= percentage <= 100:
        raise ValueError("Percentage must be between 0 and 100.")
    if not passed:
        return "F"
    for threshold, grade in [
        (90, "A+"),
        (80, "A"),
        (70, "B"),
        (60, "C"),
        (50, "D"),
        (40, "E"),
    ]:
        if percentage >= threshold:
            return grade
    return "F"


def determine_pass_status(marks):
    """Return one Boolean per student from a two-dimensional marks array."""
    return np.all(np.asarray(marks, dtype=float) >= 40, axis=1)


def calculate_student_results(data, subjects=SUBJECTS):
    """Compute marks from validated data; each subject is assumed out of 100."""
    result = data.copy(deep=True)
    marks = result[list(subjects)].to_numpy(dtype=float)
    passed = determine_pass_status(marks)
    result["total_marks"] = np.sum(marks, axis=1)
    result["average_marks"] = np.mean(marks, axis=1)
    # Equal-weight subjects out of 100 make the mean equal to the percentage.
    result["percentage"] = result["average_marks"]
    result["grade"] = [
        assign_grade(value, bool(ok)) for value, ok in zip(result["percentage"], passed)
    ]
    result["status"] = np.where(passed, "PASS", "FAIL")
    return result


def calculate_class_statistics(results):
    """Summarize validated results, using population standard deviation."""
    values = results["average_marks"].to_numpy(dtype=float)
    passed = int(results["status"].eq("PASS").sum())
    return {
        "students": len(results),
        "passed": passed,
        "failed": len(results) - passed,
        "pass_percentage": passed / len(results) * 100,
        "fail_percentage": (len(results) - passed) / len(results) * 100,
        "highest_total": float(results["total_marks"].max()),
        "lowest_total": float(results["total_marks"].min()),
        "highest_average": float(np.max(values)),
        "lowest_average": float(np.min(values)),
        "class_average": float(np.mean(values)),
        "median": float(np.median(values)),
        "population_std": float(np.std(values, ddof=0)),
    }


def analyze_subjects(results, subjects=SUBJECTS):
    """Return one summary row per subject, including its pass rate."""
    marks = results[list(subjects)]
    stats = marks.agg(["mean", "max", "min", "median"]).T.rename(
        columns={"mean": "average", "max": "highest", "min": "lowest"}
    )
    stats["population_std"] = np.std(marks.to_numpy(dtype=float), axis=0, ddof=0)
    stats["passed"] = marks.ge(40).sum()
    stats["pass_percentage"] = stats["passed"] / len(results) * 100
    return stats.rename_axis("subject").reset_index()


def analyze_departments(results):
    """Group students by department and calculate counts, means and pass rates."""
    grouped = results.assign(passed=results["status"].eq("PASS")).groupby(
        "department", sort=True
    )
    stats = grouped.agg(
        student_count=("student_id", "size"),
        average_marks=("average_marks", "mean"),
        pass_count=("passed", "sum"),
    )
    stats["pass_percentage"] = stats["pass_count"] / stats["student_count"] * 100
    return stats.reset_index()


def analyze_attendance(results):
    """Return attendance metrics and low-attendance students without altering grades."""
    attendance = results["attendance"].to_numpy(dtype=float)
    averages = results["average_marks"].to_numpy(dtype=float)
    low = results.loc[results["attendance"] < 75].copy()
    correlation = None
    if len(results) > 1 and np.ptp(attendance) > 0 and np.ptp(averages) > 0:
        correlation = float(np.corrcoef(attendance, averages)[0, 1])
    return {
        "average": float(np.mean(attendance)),
        "highest": float(np.max(attendance)),
        "lowest": float(np.min(attendance)),
        "below_75_count": len(low),
        "below_75_percentage": len(low) / len(results) * 100,
        "correlation": correlation,
    }, low


def get_top_performers(results, count=5):
    """Exactly five rows where available; shared competition ranks for ties.

    Student IDs are strings and sort lexicographically, preserving leading zeros.
    """
    ranked = results.sort_values(
        ["average_marks", "total_marks", "student_id"], ascending=[False, False, True]
    ).copy()
    ranked.insert(
        0,
        "rank",
        ranked["average_marks"].rank(method="min", ascending=False).astype(int),
    )
    return ranked.head(count)


def build_report(data, results, subjects=SUBJECTS):
    """Build the same report used by the console and exported text file."""
    chunks = []

    def section(title, body):
        chunks.append(
            "\n" + "=" * 76 + "\n" + title + "\n" + "-" * 76 + "\n" + str(body)
        )

    def table(frame):
        return frame.to_string(index=False, float_format=lambda v: f"{v:.2f}")

    def metrics(values):
        return "\n".join(
            (
                f'{key.replace("_", " ").title()}: {value:.2f}'
                if isinstance(value, float)
                else f'{key.replace("_", " ").title()}: {value}'
            )
            for key, value in values.items()
        )

    info = io.StringIO()
    data.info(buf=info)
    section(
        "STUDENT PERFORMANCE ANALYTICS SYSTEM | DATASET OVERVIEW",
        f'Records: {data.shape[0]} | Columns: {data.shape[1]}\nColumns: {", ".join(data.columns)}\n\n'
        + table(data.head())
        + "\n\n"
        + info.getvalue(),
    )
    section("MISSING VALUES", data.isna().sum().to_string())
    section("BASIC DATASET STATISTICS", data.describe(include="all").to_string())
    result_columns = [
        "student_id",
        "name",
        "department",
        "total_marks",
        "average_marks",
        "percentage",
        "grade",
        "status",
    ]
    section("STUDENT RESULTS", table(results[result_columns]))
    stats = calculate_class_statistics(results)
    section("CLASS STATISTICS AND PASS / FAIL ANALYSIS", metrics(stats))
    section(
        "GRADE DISTRIBUTION",
        results["grade"].value_counts().reindex(GRADES, fill_value=0).to_string(),
    )
    subject_stats = analyze_subjects(results, subjects)
    section("SUBJECT-WISE ANALYSIS", table(subject_stats))
    section(
        "TOP 5 PERFORMERS",
        table(get_top_performers(results)[["rank", *result_columns]]),
    )
    departments = analyze_departments(results)
    section("DEPARTMENT ANALYSIS", table(departments))
    attendance, low = analyze_attendance(results)
    section(
        "ATTENDANCE ANALYSIS",
        metrics(attendance)
        + "\n\nBelow 75% attendance:\n"
        + table(
            low[
                [
                    "student_id",
                    "name",
                    "department",
                    "attendance",
                    "average_marks",
                    "status",
                ]
            ]
        ),
    )
    highest = results.loc[results["average_marks"].eq(stats["highest_average"])]
    lowest = results.loc[results["average_marks"].eq(stats["lowest_average"])]

    def names(frame):
        return ", ".join(
            f'{row["name"]} ({row["student_id"]})' for _, row in frame.iterrows()
        )

    best = subject_stats.loc[
        subject_stats["average"].eq(subject_stats["average"].max()), "subject"
    ].tolist()
    weakest = subject_stats.loc[
        subject_stats["average"].eq(subject_stats["average"].min()), "subject"
    ].tolist()
    insights = [
        f'{stats["passed"]} passed and {stats["failed"]} failed out of {len(results)} students.',
        f'Class average: {stats["class_average"]:.2f}/100.',
        f"Highest performer(s): {names(highest)}.",
        f"Lowest performer(s): {names(lowest)}.",
        f'Strongest subject(s) by mean: {", ".join(best)}.',
        f'Weakest subject(s) by mean: {", ".join(weakest)}.',
        f'Subject mean spread: {subject_stats["average"].max() - subject_stats["average"].min():.2f} marks.',
        "Students needing subject improvement: "
        + (names(results.loc[results["status"].eq("FAIL")]) or "None")
        + ".",
        "Attendance below 75% is an observation, not an exam failure rule.",
        "Standard deviation uses the population formula (ddof=0).",
        "Correlation indicates association only, not causation. None means undefined.",
    ]
    if len(departments) > 1:
        for label, value in [
            ("Highest", departments["average_marks"].max()),
            ("Lowest", departments["average_marks"].min()),
        ]:
            items = departments.loc[
                departments["average_marks"].eq(value), "department"
            ]
            insights.append(
                f'{label} department average: {", ".join(items)} ({value:.2f}).'
            )
    else:
        insights.append(
            "Only one department; no cross-department comparison is possible."
        )
    section("FINAL PERFORMANCE SUMMARY", "\n".join(insights))
    return "\n".join(chunks) + "\n"


def export_results(results, report, output_dir, subjects=SUBJECTS):
    """Write the three CSV reports and full text analysis as UTF-8."""
    path = Path(output_dir)
    path.mkdir(parents=True, exist_ok=True)
    for name, frame in [
        ("student_results", results),
        ("subject_analysis", analyze_subjects(results, subjects)),
        ("department_analysis", analyze_departments(results)),
    ]:
        frame.to_csv(
            path / f"{name}.csv", index=False, encoding="utf-8", float_format="%.10g"
        )
    (path / "performance_summary.txt").write_text(report, encoding="utf-8")


def display_summary(report):
    print(report)
