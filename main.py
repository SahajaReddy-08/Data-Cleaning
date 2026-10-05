import argparse
import os
import sys
from src.utils import load_dataset, inspect_data, print_summary
from src.cleaner import DataCleaner


def run_pipeline(input_path: str, output_path: str = None) -> None:
    """Run data inspection and cleaning pipeline."""
    if not output_path:
        base_name = os.path.basename(input_path)
        output_path = os.path.join("data", "processed", f"cleaned_{base_name}")

    print(f"\n[1/4] Loading dataset: {input_path}")
    df = load_dataset(input_path)

    print("\n[2/4] Initial Data Inspection:")
    summary_before = inspect_data(df)
    print_summary(summary_before)

    print("\n[3/4] Running Cleaning Steps...")
    cleaner = (
        DataCleaner(df)
        .clean_column_names()
        .trim_whitespace()
        .remove_duplicates()
        # Example strategy: drop or fill nulls (adjust based on your dataset)
        .handle_missing_values(strategy="drop")
    )

    cleaned_df = cleaner.get_data()

    print("\n[4/4] Post-Cleaning Data Inspection:")
    summary_after = inspect_data(cleaned_df)
    print_summary(summary_after)

    cleaner.export(output_path)
    print("\nPipeline complete!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the Data Cleaning pipeline.")
    parser.add_argument(
        "--input",
        "-i",
        type=str,
        default="data/raw/sample.csv",
        help="Path to raw dataset (CSV, Excel, etc.)"
    )
    parser.add_argument(
        "--output",
        "-o",
        type=str,
        default=None,
        help="Path to save cleaned dataset (default: data/processed/cleaned_<filename>)"
    )

    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"Error: Input file '{args.input}' not found.")
        print("Please place your raw dataset in 'data/raw/' or specify with --input <path>.")
        sys.exit(1)

    run_pipeline(args.input, args.output)
