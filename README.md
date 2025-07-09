# CSV Comparison Tool

This repository provides a powerful Python script to compare two CSV files with identical headers, offering an in-depth difference report and the ability to output a new CSV containing the differing rows.

## Features
- Compares two CSV files with the same column headers
- Detects rows only in the first or second file
- Identifies rows with the same key but different values (shows column-level differences)
- Outputs a detailed text report
- Optionally creates a new CSV file with all differing rows
- Highly configurable via `config.yaml` (key columns, output paths, case sensitivity, etc.)

## Requirements
- Python 3.7+
- [PyYAML](https://pypi.org/project/PyYAML/)

Install dependencies:
```bash
pip install pyyaml
```

## Usage

1. **Prepare your CSV files**: Ensure both files have the same column headers.
2. **Edit `config.yaml`**: Set your unique key columns and other options as needed.
3. **Run the script:**

```bash
python compare_csvs.py file1.csv file2.csv config.yaml
```

- `file1.csv` and `file2.csv` are the paths to your CSV files.
- `config.yaml` is the configuration file (see below).

## Configuration (`config.yaml`)

Example:
```yaml
# List of columns to use as the unique key for row comparison
key_columns:
  - id  # Change to your unique column(s), or remove to use all columns

# Whether to output a CSV file with the differing rows
output_diff_csv: true

# Path for the output CSV file containing differing rows
diff_csv_path: diff_output.csv

# Path for the detailed text report
report_path: diff_report.txt

# Whether to treat values as case sensitive
case_sensitive: true

# Whether to ignore row order (default: true)
ignore_order: true
```

## Output
- **Detailed report**: By default, written to `diff_report.txt`.
- **Diff CSV**: By default, written to `diff_output.csv` (if enabled in config).

## Example
```bash
python compare_csvs.py data1.csv data2.csv config.yaml
```

## License
MIT 