import pandas as pd
import os
from pathlib import Path
import gc
from tqdm import tqdm
import argparse


def merge_cr_dates_fast(input_path: str, output_folder: str) -> None:
    """
    Efficiently merge per-date CSV files into one dataset by streaming and aligning columns.

    Args:
        input_path (str): Path to the folder containing per-date CSV files.
        output_folder (str): Path to the folder where the merged CSV will be saved.

    The merged file will be named 'call_reports_all_dates.csv' in the specified output_folder.
    """
    input_dir = Path(input_path)
    output_dir = Path(output_folder)
    output_dir.mkdir(parents=True, exist_ok=True)
    output_csv = output_dir / 'call_reports_all_dates.csv'

    # 1) Discover all CSVs
    files = sorted(input_dir.glob("*.csv"))
    if not files:
        raise RuntimeError(f"No CSV files found in: {input_dir}")

    # 2) Build the union of all column names
    master_cols_set = set()
    for f in tqdm(files, desc="Inspecting headers", unit="file"):
        cols = pd.read_csv(f, nrows=0).columns
        master_cols_set.update(cols)
    master_cols = list(master_cols_set)

    # 3) Initialize output with header only
    pd.DataFrame(columns=master_cols).to_csv(output_csv, index=False)

    # 4) Read each file, align columns, parse Date, and append
    for f in tqdm(files, desc="Merging files", unit="file"):
        df_part = pd.read_csv(f, low_memory=False)
        df_part = df_part.reindex(columns=master_cols)
        df_part["Date"] = pd.to_datetime(df_part["Date"], format="%m%d%Y")
        df_part.to_csv(output_csv, 
                       mode="a", header=False, index=False)
        del df_part
        gc.collect()

    print(f"Merged file saved to: {output_csv}")
