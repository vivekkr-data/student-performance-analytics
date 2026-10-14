"""Synthetic edge cases and reference checks for the bundled Kaggle CSV."""

from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import pandas as pd
from functions import (
    analyze_attendance,
    analyze_departments,
    analyze_subjects,
    assign_grade,
    build_report,
    calculate_class_statistics,
    calculate_student_results,
    export_results,
    get_top_performers,
    load_student_data,
    validate_student_data,
)


def fixture():
    # Five controlled cases repeated four times make an independent 20-row oracle.
    return pd.DataFrame(
        {
            "student_id": [f"T{i:02}" for i in range(20)],
            "name": [f"Test Student {i}" for i in range(20)],
            "department": ["Test-A", "Test-B"] * 10,
            "attendance": [75, 74, 100, 0, 80] * 4,
            "python_marks": [90, 40, 100, 39, 60] * 4,
            "ml_marks": [80, 40, 100, 100, 60] * 4,
        }
    )


class AnalyticsTests(unittest.TestCase):
    def setUp(self):
        self.data = validate_student_data(fixture())
        self.results = calculate_student_results(self.data)

    def test_calculations_independent(self):
        for (_, raw), (_, actual) in zip(self.data.iterrows(), self.results.iterrows()):
            total = float(raw.python_marks) + float(raw.ml_marks)
            self.assertEqual(actual.total_marks, total)
            self.assertEqual(actual.average_marks, total / 2)
            self.assertAlmostEqual(actual.percentage, total / 200 * 100)

    def test_grade_boundaries(self):
        for boundary, grade in [
            (40, "E"),
            (50, "D"),
            (60, "C"),
            (70, "B"),
            (80, "A"),
            (90, "A+"),
        ]:
            with self.subTest(boundary=boundary):
                self.assertEqual(assign_grade(boundary), grade)
                self.assertNotEqual(assign_grade(boundary - 0.001), grade)
        self.assertEqual(assign_grade(100), "A+")
        self.assertEqual(assign_grade(0), "F")

    def test_invalid_grade(self):
        for value in [-1, 101, float("nan"), float("inf")]:
            with self.assertRaises(ValueError):
                assign_grade(value)

    def test_single_subject_failure(self):
        row = self.results.iloc[3]
        self.assertEqual(row.average_marks, 69.5)
        self.assertEqual(row.status, "FAIL")
        self.assertEqual(row.grade, "F")

    def test_exact_pass_threshold(self):
        self.assertEqual(self.results.iloc[1].status, "PASS")
        self.assertEqual(self.results.iloc[1].grade, "E")

    def test_statistics_independent(self):
        stats = calculate_class_statistics(self.results)
        values = [85, 40, 100, 69.5, 60] * 4
        mean = sum(values) / 20
        std = (sum((v - mean) ** 2 for v in values) / 20) ** 0.5
        self.assertEqual(stats["class_average"], mean)
        self.assertEqual(stats["median"], 69.5)
        self.assertAlmostEqual(stats["population_std"], std)
        self.assertEqual((stats["passed"], stats["failed"]), (16, 4))
        self.assertEqual(stats["pass_percentage"], 80)
        self.assertEqual(stats["highest_total"], 200)
        self.assertEqual(stats["lowest_total"], 80)

    def test_tied_high_low(self):
        report = build_report(self.data, self.results)
        for i in [2, 7, 12, 17, 1, 6, 11, 16]:
            self.assertIn(f"Test Student {i} (T{i:02})", report)

    def test_top_five_ties(self):
        top = get_top_performers(self.results)
        self.assertEqual(top.student_id.tolist(), ["T02", "T07", "T12", "T17", "T00"])
        self.assertEqual(top["rank"].tolist(), [1, 1, 1, 1, 5])

    def test_subject_averages(self):
        subjects = analyze_subjects(self.results)
        self.assertAlmostEqual(subjects.iloc[0]["average"], 65.8)
        self.assertEqual(subjects.iloc[1]["average"], 76)
        self.assertEqual(subjects.passed.tolist(), [16, 20])

    def test_department_aggregation(self):
        dept = analyze_departments(self.results)
        self.assertEqual(dept.student_count.tolist(), [10, 10])
        self.assertEqual(dept.pass_count.tolist(), [8, 8])
        self.assertEqual(dept.average_marks.tolist(), [70.9, 70.9])

    def test_attendance_boundary(self):
        stats, low = analyze_attendance(self.results)
        self.assertEqual(stats["below_75_count"], 8)
        self.assertEqual(stats["below_75_percentage"], 40)
        self.assertEqual(stats["average"], 65.8)
        self.assertTrue((low.attendance < 75).all())

    def test_undefined_correlation(self):
        data = self.results.copy()
        data.attendance = 75
        self.assertIsNone(analyze_attendance(data)[0]["correlation"])

    def test_missing_columns(self):
        with self.assertRaises(ValueError):
            validate_student_data(self.data.drop(columns="name"))

    def test_duplicate_ids(self):
        data = fixture()
        data.loc[1, "student_id"] = data.loc[0, "student_id"]
        with self.assertRaises(ValueError):
            validate_student_data(data)

    def test_missing_text(self):
        for value in ["", "   ", None]:
            data = fixture()
            data.loc[0, "name"] = value
            with self.assertRaises(ValueError):
                validate_student_data(data)

    def test_whitespace_rejected(self):
        data = fixture()
        data.loc[0, "student_id"] = " T00 "
        with self.assertRaises(ValueError):
            validate_student_data(data)

    def test_invalid_numbers(self):
        for column in ["python_marks", "ml_marks", "attendance"]:
            for value in ["oops", None, -1, 101, float("inf")]:
                data = fixture().astype({column: object})
                data.loc[0, column] = value
                with self.subTest(column=column, value=value), self.assertRaises(
                    ValueError
                ):
                    validate_student_data(data)

    def test_insufficient_records(self):
        for size in [0, 1, 19]:
            with self.assertRaises(ValueError):
                validate_student_data(fixture().head(size))

    def test_input_not_mutated(self):
        before = fixture()
        copy = before.copy(deep=True)
        calculate_student_results(validate_student_data(before))
        pd.testing.assert_frame_equal(before, copy)

    def test_alternative_subjects(self):
        data = fixture().rename(
            columns={"python_marks": "math_marks", "ml_marks": "science_marks"}
        )
        subjects = ["math_marks", "science_marks"]
        results = calculate_student_results(
            validate_student_data(data, subjects), subjects
        )
        self.assertEqual(results.iloc[0].total_marks, 170)
        self.assertEqual(analyze_subjects(results, subjects).shape[0], 2)

    def test_invalid_subject_selection(self):
        for columns in [[], ["attendance"], ["python_marks", "python_marks"]]:
            with self.assertRaises(ValueError):
                validate_student_data(fixture(), columns)

    def test_reserved_columns(self):
        with self.assertRaises(ValueError):
            validate_student_data(fixture().assign(grade="A"))

    def test_single_department(self):
        results = self.results.copy()
        results.department = "Only"
        self.assertIn(
            "no cross-department comparison", build_report(self.data, results)
        )

    def test_csv_loading_and_exports(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "input.csv"
            fixture().to_csv(path, index=False)
            loaded = validate_student_data(load_student_data(path))
            self.assertEqual(loaded.student_id.iloc[0], "T00")
            output = Path(temp) / "out"
            report = build_report(loaded, self.results)
            export_results(self.results, report, output)
            self.assertEqual(len(pd.read_csv(output / "student_results.csv")), 20)
            self.assertEqual(len(pd.read_csv(output / "subject_analysis.csv")), 2)
            self.assertEqual(len(pd.read_csv(output / "department_analysis.csv")), 2)
            self.assertEqual((output / "performance_summary.txt").read_text(), report)

    def test_empty_missing_malformed_csv(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "data.csv"
            with self.assertRaises(ValueError):
                load_student_data(path)
            for content in ["", "a,a\n1,2\n", 'a,b\n"unclosed']:
                path.write_text(content)
                with self.assertRaises(ValueError):
                    load_student_data(path)

    def test_export_error(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "file"
            path.write_text("occupied")
            with self.assertRaises(OSError):
                export_results(self.results, "report", path)

    def test_cli_integration_synthetic_only(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "fixture.csv"
            fixture().to_csv(path, index=False)
            main = Path(__file__).resolve().parents[1] / "main.py"
            run = subprocess.run(
                [
                    sys.executable,
                    str(main),
                    "--data",
                    str(path),
                    "--output",
                    str(Path(temp) / "out"),
                ],
                text=True,
                capture_output=True,
                cwd=temp,
            )
            self.assertEqual(run.returncode, 0, run.stderr)
            self.assertIn("Class Average: 70.90", run.stdout)
            self.assertIn("Passed: 16", run.stdout)
            self.assertIn("FINAL PERFORMANCE SUMMARY", run.stdout)
            failed = subprocess.run(
                [sys.executable, str(main), "--data", str(Path(temp) / "missing.csv")],
                text=True,
                capture_output=True,
            )
            self.assertEqual(failed.returncode, 1)
            self.assertNotIn("Traceback", failed.stderr)

    def test_csv_field_counts(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "malformed.csv"
            for content in ["a,b\n1,2,3\n", "a,b\n1\n", "a,b\n\n", ",b\n1,2\n"]:
                with self.subTest(content=content):
                    path.write_text(content)
                    with self.assertRaises(ValueError):
                        load_student_data(path)

    def test_csv_quoted_names_and_leading_zero_ids(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "quoted.csv"
            data = fixture()
            data.loc[0, "name"] = "Test, Student"
            data.loc[0, "student_id"] = "001"
            data.to_csv(path, index=False)
            loaded = validate_student_data(load_student_data(path))
            self.assertEqual(loaded.loc[0, "name"], "Test, Student")
            self.assertEqual(loaded.loc[0, "student_id"], "001")

    def test_metadata_cannot_be_subjects(self):
        data = fixture().assign(age=19, year=2, projects_completed=3)
        for column in ["age", "year", "projects_completed"]:
            with self.subTest(column=column), self.assertRaises(ValueError):
                validate_student_data(data, [column])

    def test_bundled_dataset_reference_results(self):
        source = Path(__file__).resolve().parents[1] / "students.csv"
        data = validate_student_data(load_student_data(source))
        results = calculate_student_results(data)
        stats = calculate_class_statistics(results)
        self.assertEqual(len(data), 30)
        self.assertEqual((stats["passed"], stats["failed"]), (30, 0))
        self.assertAlmostEqual(stats["class_average"], 82.35)
        self.assertEqual(
            get_top_performers(results)["student_id"].tolist(),
            ["22", "29", "11", "19", "2"],
        )
        self.assertEqual(analyze_attendance(results)[0]["below_75_count"], 7)


if __name__ == "__main__":
    unittest.main()
