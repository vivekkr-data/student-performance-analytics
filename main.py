"""Run with: python main.py --data students.csv --output outputs"""
import argparse
from pathlib import Path
import sys
from functions import (SUBJECTS, load_student_data, validate_student_data,
                       calculate_student_results, build_report, export_results, display_summary)


def main(argv=None):
    base = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description='Student performance analytics; subjects must each be out of 100.')
    parser.add_argument('--data', type=Path, default=base / 'students.csv')
    parser.add_argument('--output', type=Path, default=base / 'outputs')
    parser.add_argument('--subjects', nargs='+', default=list(SUBJECTS))
    args = parser.parse_args(argv)
    try:
        raw = load_student_data(args.data)
        data = validate_student_data(raw, args.subjects)
        results = calculate_student_results(data, args.subjects)
        report = build_report(raw, results, args.subjects)
        export_results(results, report, args.output, args.subjects)
    except (ValueError, OSError) as error:
        print(f'Error: {error}', file=sys.stderr)
        return 1
    display_summary(report)
    print(f'Reports saved to: {args.output.resolve()}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
