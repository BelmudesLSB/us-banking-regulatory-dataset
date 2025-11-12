# pipeline.py
import os
import sys
import argparse

from ingest_raw_ffiec_cdr import ingest
from merge_cr_dates_fast import merge_cr_dates_fast
from call_reports_cleaner import CallReportsCleaner
from add_external_information import add_external_data_attributes, add_external_data_tic
from mappings import mappings
from aux_functions import extract_variables_from_mappings


def run_pipeline(base_path):
    ### Define project paths:

    # raw_data: 
    raw_data       = os.path.join(base_path, "raw")
    # raw_ffiec: where the extracted FFIEC CDR folders are located:
    raw_ffiec      = os.path.join(base_path, "raw", "ffiec", "extracted", "cdr")
    # intermediate: where the per-date merged CSVs will be saved:
    intermediate   = os.path.join(base_path, "intermediate", "ffiec_cdr_all_dates")
    # merged_output: where the final merged CSV will be saved:
    merged_output  = os.path.join(base_path, "intermediate", "ffiec_cdr_all_dates_merged")
    # Atrributes files:
    attributes_dir = os.path.join(base_path, "raw", "ffiec", "extracted", "nic")
    # Clean data path:
    clean_data = os.path.join(base_path, "clean")

    # Step 1: Ingest raw FFIEC schedules into per-date CSVs
    print("Step 1: Ingesting raw FFIEC schedules…")
    ingest(raw_ffiec, intermediate)

    # Step 2: Merge all per-date CSVs into a single dataset
    print("Step 2: Merging per-date CSVs into call_reports_all_dates.csv…")
    merge_cr_dates_fast(intermediate, merged_output)

    # Step 3: Clean and select variables
    print("Step 3: Selecting variables from merged call reports…")
    # Extract all variables defined in mappings.py:
    all_variables_needed = extract_variables_from_mappings(mappings)
    # Create a CallReportsCleaner instance:
    crc = CallReportsCleaner(merged_output, all_variables_needed)
    # Construct the dataset with the new definitions in mappings.py:
    df = crc.construct_definitions(mappings)

    # Step 4: Add external data attributes
    print("Step 4: Adding external data attributes…")
    df = add_external_data_tic(raw_data, df)
    df = add_external_data_attributes(attributes_dir, df)
    
    # Step 5: Store dataset as csv in clean path as csv:
    output_file = os.path.join(clean_data, "final_call_reports_dataset.csv")
    df.to_csv(output_file, index=False)
    print(f"Pipeline finished! Saved to {output_file}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run full Call Reports pipeline.")
    parser.add_argument(
        "base_path",
        help="Base data directory (e.g. C:\\Users\\...\\banking_project\\data)"
    )
    args = parser.parse_args()

    run_pipeline(args.base_path)
