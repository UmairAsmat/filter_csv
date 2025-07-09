import csv
import yaml
import sys
from collections import defaultdict

# Load configuration
def load_config(config_path):
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def read_csv(file_path):
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        rows = list(reader)
        return rows, reader.fieldnames

def compare_csvs(file1, file2, config):
    rows1, headers1 = read_csv(file1)
    rows2, headers2 = read_csv(file2)

    if not headers1 or not headers2:
        raise ValueError('One or both CSV files are missing headers!')
    if headers1 != headers2:
        raise ValueError('CSV files have different headers!')

    key_columns = config.get('key_columns', headers1 if headers1 else [])
    output_diff_csv = config.get('output_diff_csv', True)
    diff_csv_path = config.get('diff_csv_path', 'diff_output.csv')
    report_path = config.get('report_path', 'diff_report.txt')
    case_sensitive = config.get('case_sensitive', True)
    ignore_order = config.get('ignore_order', False)

    def row_key(row):
        return tuple(row[k] if case_sensitive else row[k].lower() for k in key_columns)

    map1 = {row_key(row): row for row in rows1}
    map2 = {row_key(row): row for row in rows2}

    only_in_1 = [row for k, row in map1.items() if k not in map2]
    only_in_2 = [row for k, row in map2.items() if k not in map1]
    in_both = [k for k in map1 if k in map2]

    changed_rows = []
    for k in in_both:
        diffs = {}
        for col in headers1:
            v1 = map1[k][col]
            v2 = map2[k][col]
            if v1 != v2:
                diffs[col] = (v1, v2)
        if diffs:
            changed_rows.append({'key': k, 'diffs': diffs})

    # Write report
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write('Rows only in first file:\n')
        for row in only_in_1:
            f.write(str(row) + '\n')
        f.write('\nRows only in second file:\n')
        for row in only_in_2:
            f.write(str(row) + '\n')
        f.write('\nRows with changed values:\n')
        for change in changed_rows:
            f.write(f'Key: {change["key"]}\n')
            for col, (v1, v2) in change['diffs'].items():
                f.write(f'  {col}: {v1} -> {v2}\n')
            f.write('\n')

    # Write diff CSV if enabled
    if output_diff_csv:
        with open(diff_csv_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=headers1 if headers1 else [])
            writer.writeheader()
            for row in only_in_1 + only_in_2:
                writer.writerow(row)

    print(f'Detailed report written to {report_path}')
    if output_diff_csv:
        print(f'Diff CSV written to {diff_csv_path}')

def main():
    if len(sys.argv) != 4:
        print('Usage: python compare_csvs.py <csv1> <csv2> <config.yaml>')
        sys.exit(1)
    file1, file2, config_path = sys.argv[1:4]
    config = load_config(config_path)
    compare_csvs(file1, file2, config)

if __name__ == '__main__':
    main() 