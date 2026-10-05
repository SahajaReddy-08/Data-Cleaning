import os
import pandas as pd


def load_dataset(file_path: str) -> pd.DataFrame:
    """Load a dataset from CSV or Excel file."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".csv":
        return pd.read_csv(file_path)
    elif ext in [".xls", ".xlsx"]:
        return pd.read_excel(file_path)
    elif ext == ".json":
        return pd.read_json(file_path)
    elif ext == ".parquet":
        return pd.read_parquet(file_path)
    else:
        raise ValueError(f"Unsupported file format: {ext}")


def inspect_data(df: pd.DataFrame) -> dict:
    """Generate a quick structural and quality summary of the dataframe."""
    summary = {
        "rows": len(df),
        "columns": len(df.columns),
        "duplicate_rows": int(df.duplicated().sum()),
        "missing_values_total": int(df.isna().sum().sum()),
        "columns_with_missing": df.isna().sum()[df.isna().sum() > 0].to_dict(),
        "column_types": {col: str(dtype) for col, dtype in df.dtypes.items()}
    }
    return summary


def print_summary(summary: dict) -> None:
    """Print readable inspection report."""
    print("=" * 50)
    print("DATA QUALITY SUMMARY")
    print("=" * 50)
    print(f"Total Rows:        {summary['rows']}")
    print(f"Total Columns:     {summary['columns']}")
    print(f"Duplicate Rows:    {summary['duplicate_rows']}")
    print(f"Missing Values:    {summary['missing_values_total']}")
    if summary['columns_with_missing']:
        print("\nColumns with Missing Values:")
        for col, count in summary['columns_with_missing'].items():
            pct = (count / summary['rows']) * 100 if summary['rows'] > 0 else 0
            print(f"  - {col}: {count} ({pct:.1f}%)")
    else:
        print("\nNo missing values detected.")
    print("=" * 50)
