from email import header
import pandas as pd
from pandas.api.types import is_numeric_dtype
from tqdm import tqdm
import numpy as np
import os

from pyparsing import col

class CallReportsCleaner:
    def __init__(self, folder_path, variables=None, verbose=True):
        """
        Initialize the analysis class with the folder path where 'call_reports_all_dates.csv' is stored.

        Parameters:
          folder_path (str): Path to the folder containing 'call_reports_all_dates.csv'.

        Attributes:
          df_selected (pd.DataFrame): DataFrame to hold the selected variables for analysis.
          self.essential_vars (list): List of essential variables to always include in the analysis.
        """
        
        self.folder_path = folder_path
        # Build full path for the call_reports_all_dates.csv file.
        self.file_path = os.path.join(folder_path, "call_reports_all_dates.csv")

        # Define the essential_variables.
        self.essential_vars = ['IDRSSD', 'Financial Institution Name', 'Date']

        # Initialize dataframes to None.
        self.df_selected = None

        # store verbosity preference
        self.verbose = verbose

        # Run select_variables straigh after initialization:
        self.select_variables(variables)

        

    def select_variables(self, variables=None):
        """
        Load and clean a subset of call report columns.

        1) Build vars_requested_by_user: union of essential_vars + any user-specified.
        2) Read CSV header to discover available columns.
        3) Expand to include ANY suffix on each base variable (e.g. _x, _y, _z, ...).
        4) Warn if a requested base (and its variants) are completely absent.
        5) Read only the selected columns into memory (minimizing I/O).
        6) Convert 'Date' to datetime for time-based operations.
        7) For each base, sequentially merge variants into one series using combine_first,
           checking overlaps for mismatches, and then drop raw variants.
        8) Reorder so essential_vars appear first, then all other columns.

        Parameters:
          variables (list, optional): Additional variable names to select.

        Returns:
          DataFrame: The cleaned and ordered DataFrame of selected variables.
        """
        # 1) Build the initial request list
        if variables is None:
            vars_requested_by_user = self.essential_vars.copy()
        else:
            vars_requested_by_user = list(set(self.essential_vars + variables))

        # 2) Peek at header
        try:
            cols_available = pd.read_csv(self.file_path, nrows=0).columns
        except Exception as e:
            raise IOError(f"Error reading file header from {self.file_path}: {e}")

        # 3) Expand to include any suffix variants of each requested base
        vars_requested_by_user_available_extended = [
            col for col in cols_available
            if any(col == base or col.startswith(f"{base}_") for base in vars_requested_by_user)
        ]

        # 4) Warn for bases that didn’t match anything (even with suffixes)
        missing = [
            base for base in vars_requested_by_user
            if not any(col == base or col.startswith(f"{base}_") for col in vars_requested_by_user_available_extended)
        ]
        if missing:
            print(
                "Warning: The following requested variables (and any suffix variants) "
                "are not in the data and will be skipped:", missing
            )

        # 5) Load only the extended set of columns
        self.df_selected = pd.read_csv(
            self.file_path,
            usecols=vars_requested_by_user_available_extended
        )

        # 6) Coerce Date
        self.df_selected['Date'] = pd.to_datetime(
            self.df_selected['Date'],
            errors='coerce'
        )

        # 7) Sequentially merge each suffix‐variant into its base,
        cols = list(self.df_selected.columns)
        base_vars = {c.split('_', 1)[0] for c in cols}

        for base in base_vars:
            # refresh the list of columns
            cols = list(self.df_selected.columns)

            # find all variants of this base
            variants = [c for c in cols if c == base or c.startswith(f"{base}_")]
            if len(variants) <= 1:
                continue

            # ensure the “pure” base comes first
            variants = [v for v in variants if v == base] + [v for v in variants if v != base]
            if self.verbose:
                print(f"Info: Merging variants for base '{base}': {variants}")
            # start merging
            combined = self.df_selected[variants[0]].copy()
            for var in variants[1:]:
                if self.verbose:
                    print(f"Info: Merging {var} into {base}")
                # at this point var is guaranteed to be in self.df_selected.columns
                # because we built variants from cols
                overlap = combined.notna() & self.df_selected[var].notna()
                if (combined[overlap] != self.df_selected[var][overlap]).any():
                    print(f"Warning: mismatch between {base} and {var} in {overlap.sum()} rows")
                    raise ValueError(
                        f"Mismatch detected between {base} and {var}. "
                        "Please check the data for inconsistencies."
                    )
                else:
                    if self.verbose:
                        print(f"Info: {base} and {var} match in all overlapping rows.")

                combined = combined.combine_first(self.df_selected[var])

            # write back the merged series
            self.df_selected[base] = combined

            # now drop all the raw suffix variants
            to_drop = [v for v in variants if v != base]
            self.df_selected.drop(columns=to_drop, inplace=True)

        # 8) Finally, reorder so essential_vars come first, then everything else
        all_cols = list(self.df_selected.columns)
        rest     = [c for c in all_cols if c not in self.essential_vars]
        self.df_selected = self.df_selected[self.essential_vars + rest]

        # substitute spaces for underscores in column names and get rid of uppercase
        self.df_selected.columns = [col.replace('_', ' ').lower() for col in self.df_selected.columns]

        #! There is no need to return self.df_selected, as it is an attribute of the class
        return None
    
    @staticmethod
    def combine_cols(df, first_col, second_col, method, skip_na=True):
        """
        Combine two columns in a DataFrame based on the specified method.

        Parameters:
          df (pd.DataFrame): The DataFrame containing the columns to combine.
          first_col (str or list): The name of the first column to combine.
          second_col (str): The name of the second column to combine.
          method (str): The method to use for combining the columns.
          skip_na (bool): Whether to skip NA values when combining.

        Returns:
          pd.Series: A Series containing the combined values based on the specified method.

        Methods:
            - "min": Returns the minimum value between the two columns.
            - "max": Returns the maximum value between the two columns.
            - "mean": Returns the mean value between the two columns.
            - "sum": Returns the sum of the two columns, treating NaNs as zero if skip_na is True.
            - "first": Returns the first column, falling back to the second if the first is NaN.
            - "secondary": Returns the second column, falling back to the first if the second is NaN.
            - "rename": Returns the first column, effectively renaming it.
            - "ratio": Returns the ratio of the first column to the second, treating NaNs as zero if skip_na is True.
            - "ytd_diff": Returns the year-to-date difference of the first column, filling NaNs with the first column.
        """
        if method == "sum":
            # determine which columns to sum
            if isinstance(first_col, (list, tuple)):
                cols = list(first_col)
            else:
                cols = [first_col, second_col] if second_col else [first_col]
            # check that they all exist
            missing = [c for c in cols if c not in df.columns]
            if missing:
                raise KeyError(f"Cannot sum columns, these are missing: {missing}")
            # perform the sum
            return df[cols].sum(axis=1, skipna=skip_na)
        
        if (first_col in df.columns) and (second_col is None or second_col in df.columns):        
            if method == "min":
                return df[[first_col, second_col]].min(axis=1, skipna=skip_na)
            elif method == "max":
                return df[[first_col, second_col]].max(axis=1, skipna=skip_na)
            elif method == "mean":
                return df[[first_col, second_col]].mean(axis=1, skipna=skip_na)
            elif method == "first":
                return df[first_col].combine_first(df[second_col])
            elif method == "secondary":
                return df[second_col].combine_first(df[first_col])
            elif method == "rename":
                return df[first_col]
            elif method == 'ratio':
                if skip_na:
                    num = df[first_col].replace(np.nan, 0)
                else:
                    num = df[first_col]
                den = df[second_col].replace(0, np.nan)
                return num / den
            elif method == 'ytd_diff':
                return df.groupby(['idrssd', df['date'].dt.year])[first_col].diff().fillna(df[first_col])
            else:
                raise ValueError(f"Unknown combine method '{method}'")
            
        else:
            # Identify exactly which column(s) are missing
            missing_columns = []
            available_columns = []
            
            if first_col not in df.columns:
                missing_columns.append(first_col)
            else:
                available_columns.append(first_col)
            
            if second_col and second_col not in df.columns:
                missing_columns.append(second_col)
            elif second_col:
                available_columns.append(second_col)
            
            # Only raise error if there are actually missing columns
            if missing_columns:
                print(f"❌ SPECIFIC MISSING COLUMNS: {missing_columns}")
                if available_columns:
                    print(f"✅ Available columns: {available_columns}")
            else:
                # This shouldn't happen, but if it does, there's a logic error
                raise ValueError(f"Logic error in combine_cols: first_col='{first_col}', second_col='{second_col}', available columns={len(df.columns)}")


    def construct_definitions(self, mappings, skip_na=True):

        """
        This method constructs new variables based on the provided mappings. 
        It handles cases where variables may switch MDRM codes on a specific date, and allows for different methods of combining columns.
        -------------------------------------- Examples --------------------------------------
        1) **Variable that changes MDRM codes** – handled with ``switch_date``
           Suppose the variable "Held-to-maturity securities" switches MDRM codes on *2019‑03‑31*:

               mappings = [
                   {
                       "new_var": "Held-to-maturity securities",
                       "first_col": "RCFD1754",
                       "second_col": "RCON1754",
                       "switch_date": "2019-03-31",
                       "first_col_post": "RCFDJJ34",
                       "second_col_post": "RCONJJ34",
                       "method": "secondary",
                   }
               ]

           The resulting series is constructed as:

               ┌────────────┬────────────────────────────────────────┐
               │ Date       │ Columns used                          │
               ├────────────┼────────────────────────────────────────┤
               │ 2018‑12‑31 │ RCFD1754   & RCON1754                 │
               │ 2019‑03‑30 │ RCFD1754   & RCON1754                 │
               │ 2019‑03‑31 │ RCFDJJ34   & RCONJJ34   ← *switch*    │
               │ 2020‑06‑30 │ RCFDJJ34   & RCONJJ34                 │
               └────────────┴────────────────────────────────────────┘

        2) **'secondary' method** – *take the second column if available, otherwise fall back to the first.*

               # Mapping
               {
                   "new_var": "Total Equity Capital",
                   "first_col": "RCFD3210",  # fallback if priority column is NaN
                   "second_col": "RCON3210", # *priority* column
                   "method": "secondary"
               }

           Row‑wise behaviour:

           ==============================  =================  =================  =================
           RCFD3210 (col1)                RCON3210 (col2)    Returned value     Explanation
           ==============================  =================  =================  =================
           1 000                          1 200              1 200              col2 present → use it
           1 000                          NaN                1 000              col2 missing → fallback
           NaN                            NaN                NaN                both missing
           ==============================  =================  =================  =================

        3) **'sum' method** – *numeric addition, treating NaNs as zero (skip_na argument controls inclusion of NaNs).*

               # Mapping
               {
                   "new_var": "Securities AC",    # amortised‑cost securities
                   "first_col": "HTM_Securities", # e.g. held‑to‑maturity (col1)
                   "second_col": "AFS_Securities",# available‑for‑sale (col2)
                   "method": "sum"
               }

           Row‑wise behaviour:

           ==================  =================  =================  =================
           HTM (col1)          AFS (col2)         Returned value     Explanation
           ==================  =================  =================  =================
           500                 300                800                500 + 300
           NaN                 300                300                treat NaN→0, 0+300
           500                 NaN                500                500+0
           NaN                 NaN                0                  both NaN→0+0
           ==================  =================  =================  =================

        4) **'ytd_diff' method** – *year‑to‑date difference, useful for variables that accumulate over the year.*
        This method calculates the difference of a variable from the start of the year to the current date, useful for variables that accumulate over the year.

        # Mapping
        {
            "new_var": "YTD_Accumulated_Variable",
            "first_col": "RCFD1234",
            "method": "ytd_diff"
        }

        Row‑wise behaviour:
        ==================  =================  =================  =================
        RCFD1234 (col1)     Returned value     Explanation
        ==================  =================  =================  =================
        100                 100                First row, no previous year data
        200                 100                Difference from previous row (200 - 100)
        300                 100                Difference from previous row (300 - 200)
        NaN                 NaN                No data available
        ==================  =================  =================  =================

        5) **'ratio' method** – *calculates the ratio of two columns, treating NaNs as zero for the numerator and avoiding division by zero in the denominator.*
        This method calculates the ratio of two columns, treating NaNs as zero for the numerator and avoiding division by zero in the denominator.

        # Mapping
        {
            "new_var": "Variable_Ratio",
            "first_col": "RCFD1234",
            "second_col": "RCON1234",
            "method": "ratio"
        }
        Row‑wise behaviour:
        ==================  =================  =================  =================
        RCFD1234 (col1)     RCON1234 (col2)    Returned value     Explanation
        ==================  =================  =================  =================
        100                 200                0.5                100 / 200
        200                 0                  NaN                200 / 0 treated as NaN
        300                 100                3.0                300 / 100
        NaN                 0                  0.0                NaN treated as 0 / 0
        ==================  =================  =================  =================
        """
        
        # Make sure df_selected is initialized
        if self.df_selected is None:
            raise ValueError("DataFrame is not initialized. Please run select_variables() first.")
        
        # Pre-create all new columns at once (avoids fragmentation warnings)
        new_vars = [m["new_var"] for m in mappings]
        nan_block = pd.DataFrame(np.nan, index=self.df_selected.index, columns=new_vars)
        self.df_constructed = pd.concat([self.df_selected.copy(), nan_block], axis=1)

        for mapping in tqdm(mappings, desc="Constructing variables"):

            new_var = mapping['new_var']

            #! (Avoid adding new columns for each iteration) print(f"Processing new_var: {new_var}")
            #self.df_constructed[new_var] = np.nan  # Initialize new variable with NaN

            # get method and columns from mapping
            method = mapping.get('method', 'first')
            first_col = mapping['first_col']

            try:
                second_col = mapping['second_col']
            except KeyError:
                second_col = None

            # get the switch_date for the mapping we are using, set default for a future date
            switch_date = pd.Timestamp(mapping.get('switch_date', '2100-01-01'))

            
            # get the time frame
            pre_mask = self.df_selected['date'] < switch_date

            # use df_constructed to create the new variable
            self.df_constructed.loc[pre_mask, new_var] = self.combine_cols(
                self.df_constructed.loc[pre_mask],
                first_col,
                second_col,
                method,
                skip_na=skip_na
            )

            if 'switch_date' in mapping:
                
                method_post = mapping.get('method_post', method)

                if 'first_col_post' not in mapping:
                    raise ValueError(
                        "Mapping must include 'first_col_post' for post-switch calculations."
                    )
                first_col_post = mapping['first_col_post']
                second_col_post = mapping.get('second_col_post', None)

                # treat the post-switch date
                post_mask = self.df_selected['date'] >= switch_date

                # use df_constructed to create the new variable after the switch date
                self.df_constructed.loc[post_mask, new_var] = self.combine_cols(
                    self.df_constructed.loc[post_mask],
                    first_col_post,
                    second_col_post,
                    method_post,
                    skip_na=skip_na
                )

        print(f"✅ Finished constructing {len(new_vars)} variables: {', '.join(new_vars)}")

        return self.df_constructed

