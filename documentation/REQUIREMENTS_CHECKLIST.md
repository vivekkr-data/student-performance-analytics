# Requirement-to-implementation checklist

| Requirement | Implementation / evidence | Status |
|---|---|---|
| Student identity, department, subject marks, attendance | functions.py: validate_student_data | Verified on 30 supplied records |
| At least 15-20 records | Minimum 20 enforced | Implemented |
| Pandas read, organization and inspection | load_student_data, build_report | Tested |
| NumPy calculations | calculate_student_results, calculate_class_statistics | Tested |
| Functions, conditions, loops | functions.py, grading loop, report loop | Implemented |
| Student totals and averages | calculate_student_results | Tested |
| Grades and pass/fail | assign_grade, determine_pass_status | Boundary-tested |
| Highest, lowest, average | calculate_class_statistics, build_report | Ties tested |
| Subject analysis | analyze_subjects | Tested |
| Top performers | get_top_performers | Sorting/ties tested |
| Clear output | build_report, display_summary | Actual CSV run verified |
| CSV exports | export_results | Tested in temporary directory |
| Department and attendance extras | analyze_departments, analyze_attendance | Tested |
| README | ../README.md | Written |
| Ten-section documentation | Project_Documentation.md/.pdf | Completed with verified results |
| Genuine Kaggle students.csv | Original uploaded archive, byte-identical copy | Included |
| Execution on supplied data | main.py; evidence/actual_run.txt | Exit 0 |
| Real execution screenshots | Optional; actual text output included | Text evidence supplied |
| Correct target repository | vivekkr-data/student-performance-analytics | Confirmed |
| Complete project on GitHub | Code, data, outputs and documentation | Included in repository |
| Google Form link submission | EWB form URL required | Pending |
| Final documentation | Ten-section report and genuine output logs | Included in repository |

No screenshot images are supplied. Genuine program output and test logs are included; the assignment marks screenshots as optional. The EWB Google Form submission remains an external student action.
