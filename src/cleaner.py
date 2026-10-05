import os
import re
import pandas as pd
from typing import List, Optional, Union


class DataCleaner:
    """
    A modular, reusable Data Cleaning pipeline.
    Customise or extend these methods for your specific dataset needs.
    """

    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()
        self.original_shape = df.shape

    def clean_column_names(self) -> "DataCleaner":
        """Convert column names to lower_snake_case and strip whitespace."""
        clean_cols = []
        for col in self.df.columns:
            name = str(col).strip().lower()
            name = re.sub(r"[^\w\s]", "", name)
            name = re.sub(r"[\s]+", "_", name)
            clean_cols.append(name)
        self.df.columns = clean_cols
        return self

    def remove_duplicates(self, subset: Optional[List[str]] = None) -> "DataCleaner":
        """Remove duplicate rows."""
        initial_count = len(self.df)
        self.df = self.df.drop_duplicates(subset=subset).reset_index(drop=True)
        removed = initial_count - len(self.df)
        print(f"[DataCleaner] Removed {removed} duplicate row(s).")
        return self

    def trim_whitespace(self) -> "DataCleaner":
        """Strip leading/trailing whitespace from all string columns."""
        str_cols = self.df.select_dtypes(include=["object", "string"]).columns
        for col in str_cols:
            self.df[col] = self.df[col].astype(str).str.strip()
            # Restore genuine NaN values if converted to 'nan'
            self.df[col] = self.df[col].replace({"nan": None, "None": None, "": None})
        return self

    def handle_missing_values(
        self,
        strategy: str = "drop",
        columns: Optional[List[str]] = None,
        fill_value: Optional[Union[str, int, float]] = None
    ) -> "DataCleaner":
        """
        Handle missing values in specified columns or all columns.
        Strategies:
          - 'drop': drops rows with nulls
          - 'mean': fills numeric nulls with column mean
          - 'median': fills numeric nulls with column median
          - 'mode': fills nulls with column mode
          - 'constant': fills with provided fill_value
        """
        cols = columns if columns is not None else self.df.columns.tolist()

        if strategy == "drop":
            self.df = self.df.dropna(subset=cols).reset_index(drop=True)
        elif strategy == "constant":
            self.df[cols] = self.df[cols].fillna(fill_value)
        elif strategy in ["mean", "median"]:
            for col in cols:
                if pd.api.types.is_numeric_dtype(self.df[col]):
                    val = self.df[col].mean() if strategy == "mean" else self.df[col].median()
                    self.df[col] = self.df[col].fillna(val)
        elif strategy == "mode":
            for col in cols:
                if not self.df[col].mode().empty:
                    self.df[col] = self.df[col].fillna(self.df[col].mode()[0])
        else:
            raise ValueError(f"Unknown missing value strategy: {strategy}")

        return self

    def parse_dates(self, columns: List[str]) -> "DataCleaner":
        """Parse columns to datetime."""
        for col in columns:
            if col in self.df.columns:
                self.df[col] = pd.to_datetime(self.df[col], errors="coerce")
        return self

    def get_data(self) -> pd.DataFrame:
        """Return the cleaned DataFrame."""
        return self.df

    def export(self, output_path: str) -> None:
        """Export the cleaned dataset to CSV or Excel."""
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        ext = os.path.splitext(output_path)[1].lower()

        if ext == ".csv":
            self.df.to_csv(output_path, index=False)
        elif ext in [".xls", ".xlsx"]:
            self.df.to_excel(output_path, index=False)
        elif ext == ".parquet":
            self.df.to_parquet(output_path, index=False)
        else:
            self.df.to_csv(output_path, index=False)

        print(f"[DataCleaner] Successfully saved cleaned data to: {output_path}")
        print(f"[DataCleaner] Initial shape: {self.original_shape} -> Cleaned shape: {self.df.shape}")
