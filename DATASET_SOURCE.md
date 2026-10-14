# Dataset provenance

Source: TSS Pandas Challenge #1, Gagan H, Kaggle (2026).
URL: https://www.kaggle.com/competitions/tss-pandas-challenge-1/data

Supplied archive: tss-pandas-challenge-1.zip.
Actual archive member: student_data.csv.
Project filename: students.csv.
Verified dimensions: 30 student records, 9 columns.
SHA-256 (original and included file): d945daff94df2c6db4801efac5e57ee9fb063f03ad909837f8c881bb370c6d82

The CSV was copied byte-for-byte, without adding, deleting or modifying records. The source website uses the spelling student-data.csv; this project records the actual archive spelling above. sample_submission.csv is a competition-answer template and is not part of the student analytics input.

All 9 source columns have zero missing values. Student IDs are unique. Observed marks and attendance fall in 0-100. Marks are analyzed under a declared 100-point project scale; the CSV does not contain explicit score maxima. The source describes this as a Pandas practice dataset. No claim of independent real-world data collection is made.

The user supplied the archive and requested inclusion in this academic repository. The archive includes no license file, and no independent dataset redistribution license could be verified on the retrievable source page. Source rights remain with their respective holders; this repository does not relicense the dataset or assert a verified open-data license.

Test records in tests/test_functions.py are separate synthetic fixtures and never replace this dataset.
