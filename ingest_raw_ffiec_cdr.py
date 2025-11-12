import pandas as pd, csv, pathlib
import os
import glob
from tqdm import tqdm
import argparse

# Create function to load schedules dealing quoting issues
def load_schedule(path):
    """
    Load a single FFIEC CDR schedule file, handling potential parsing errors due to quoting.

    Args:
        path (str): Filesystem path to the raw schedule .txt file (tab-delimited).

    Returns:
        pandas.DataFrame: A DataFrame of the schedule with an integer IDRSSD column.

    Notes:
        - We drop the first header row with metadata, reset the index, and coerce the IDRSSD column to integer.
        - Some files may include unescaped quotes, causing pandas.ParserError. In that case,
          we retry with quoting=csv.QUOTE_NONE, strip stray quotes from data, and reapply the IDRSSD conversion.
    """
    try:
        df = pd.read_csv(
            path,
            sep='\t',
            low_memory=False,
        ).drop(index=0).reset_index(drop=True)
        df['IDRSSD'] = (
            pd.to_numeric(df['IDRSSD'], errors='coerce')
            .astype('Int64')
        )
        return df
    except pd.errors.ParserError as err:
        # Handle files with unescaped quotes by disabling pandas' internal quoting
        print(f'ParserError in {path} -> {err}')
        df = pd.read_csv(
            path,
            sep='\t',
            quoting=csv.QUOTE_NONE,
            engine='python',
            #low_memory=False,
        ).drop(index=0).reset_index(drop=True)
        df = df.replace({ '"': '' }, regex=True)
        df.columns = df.columns.str.replace('"', '', regex=False)
        df['IDRSSD'] = (
            pd.to_numeric(df['IDRSSD'], errors='coerce')
            .astype('Int64')
        )
        return df

# Helper to merge all parts of a given schedule prefix
def merge_schedule_parts(prefix, date, cr_path):
    """
    Locate and merge all file parts for a given schedule and date into one DataFrame.

    Args:
        prefix (str): The schedule name prefix (e.g., 'Schedule RC', 'Bulk POR').
        date (str): The 8-digit date code corresponding to the call report cycle.
        cr_path (str): Directory where the schedule .txt files for that date reside.

    Returns:
        pandas.DataFrame: An outer-merged DataFrame combining all parts of the schedule.
                          If no files are found, returns an empty DataFrame and logs a warning.
    """
    pattern = os.path.join(cr_path, f'FFIEC CDR Call {prefix} {date}*.txt')
    files = glob.glob(pattern)
    if not files:
        print(f'Warning: no files found for schedule {prefix} on date {date}')
        return pd.DataFrame()
    dfs = [load_schedule(fp) for fp in files]
    merged = dfs[0]
    for df_part in dfs[1:]:
        merged = pd.merge(merged, df_part, on='IDRSSD', how='outer')
    return merged

# Main ingestion function
def ingest(cr_path, save_path):
    """
    Traverse all call report date folders, merge their schedules, and save a combined CSV per date.

    Args:
        cr_path (str): Root directory containing subfolders named 'FFIEC CDR Call Bulk All Schedules {date}'.
        save_path (str): Directory path where the final per-date CSV files will be written.

    Returns:
        None: Writes output files but does not return a value.

    Notes:
        - Ensures the save_path exists.
        - Uses tqdm for visual progress over dates.
        - Performs outer merges on IDRSSD to preserve all entries.
    """
    # Ensure output directory exists
    os.makedirs(save_path, exist_ok=True)
    # List available date folders by their trailing 8-digit code
    dates = [folder[-8:] for folder in os.listdir(cr_path)
             if os.path.isdir(os.path.join(cr_path, folder))]

    # Progress bar over dates
    for date in tqdm(dates, desc='Processing dates'):
        schedule_dir = os.path.join(cr_path, f'FFIEC CDR Call Bulk All Schedules {date}')
        if not os.path.isdir(schedule_dir):
            print(f'Warning: directory not found for date {date}')
            continue

        # Merge all schedule parts robustly
        rc   = merge_schedule_parts('Schedule RC', date, schedule_dir)
        rcci = merge_schedule_parts('Schedule RCCI', date, schedule_dir)
        rca  = merge_schedule_parts('Schedule RCA', date, schedule_dir)
        rcg  = merge_schedule_parts('Schedule RCG', date, schedule_dir)
        rce1 = merge_schedule_parts('Schedule RCEI', date, schedule_dir)
        por  = merge_schedule_parts('Bulk POR', date, schedule_dir)
        rck  = merge_schedule_parts('Schedule RCK', date, schedule_dir)
        ri   = merge_schedule_parts('Schedule RI', date, schedule_dir)
        ribi = merge_schedule_parts('Schedule RIBI', date, schedule_dir)
        rco  = merge_schedule_parts('Schedule RCO', date, schedule_dir)
        rcb  = merge_schedule_parts('Schedule RCB', date, schedule_dir)

        # Merge all schedules on 'IDRSSD' without losing any rows
        dt = rc
        for df in [rcci, rca, rcg, rce1, por, rck, ri, ribi, rco, rcb]:
            if not df.empty:
                dt = pd.merge(dt, df, on='IDRSSD', how='outer')
        dt['Date'] = date

        # Save the merged data
        output_file = os.path.join(save_path, f'{date}.csv')
        dt.to_csv(output_file, index=False)

