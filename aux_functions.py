import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import re

def extract_variables_from_mappings(mappings):
    """
    Extract all RCON and RCFD variables (8 characters) from mappings.
    Returns a sorted list of unique uppercase variables.
    """
    variables = set()
    
    def extract_from_value(value):
        """Extract variables from a single value (string or tuple)."""
        if isinstance(value, str):
            # Find all 8-character patterns starting with rcon or rcfd (case insensitive)
            matches = re.findall(r'\b(rcon[a-z0-9]{4}|rcfd[a-z0-9]{4}|riad[a-z0-9]{4})\b', value.lower())
            variables.update(matches)
        elif isinstance(value, (list, tuple)):
            # Handle tuples/lists of variables
            for item in value:
                if isinstance(item, str) and len(item) == 8:
                    if item.lower().startswith(('rcon', 'rcfd')):
                        variables.add(item.lower())
    
    # Iterate through all mappings
    for mapping in mappings:
        if isinstance(mapping, dict):
            for key, value in mapping.items():
                if key in ['first_col', 'second_col', 'first_col_post', 'second_col_post']:
                    extract_from_value(value)
    
    # Convert to uppercase and return sorted list
    return sorted([var.upper() for var in variables])


def create_ticker_df(path_wrds: str, 
                           write_txt: bool = False):
    """
    Build WRDS-ready PERMCO list from the NY Fed crosswalk, read the WRDS export,
    identify PERMCOs that changed ticker, and merge in the Call Reports RSSD 'entity'.

    Parameters
    ----------
    path_wrds : str
        Folder containing:
          - 'permco_idrssd_xwalk.csv'  (with columns: ['permco','entity'])
          - 'wrds_data.csv'            (downloaded from WRDS using permco_codes.txt)

    Side effect
    -----------
    Writes 'permco_codes.txt' in the same folder with the unique PERMCOs to paste into WRDS.

    Returns
    -------
    df_changed_ticker : pd.DataFrame
        Rows for PERMCOs with >1 ticker, giving the first date each ticker appears
        per (permco, permno). Columns: ['permco','permno','tic','first_date'].
    dt : pd.DataFrame
        WRDS panel merged with the crosswalk on 'permco' to include 'entity'.
        (Same rows/cols as your filtered WRDS panel plus the 'entity' column.)
    """
    # ------------------------------------------------------------------
    # 0) READ CROSSWALK AND KEEP ONLY PERMCO, ENTITY
    # This was downloaded from the NY Fed: https://www.newyorkfed.org/research/banking_research/datasets.html
    # ------------------------------------------------------------------
    permco_idrssd_xwalk = pd.read_csv(os.path.join(path_wrds, 'permco_idrssd_xwalk.csv'))
    permco_idrssd_xwalk = permco_idrssd_xwalk[permco_idrssd_xwalk["dt_end"]>20010101]
    permco_idrssd_xwalk = permco_idrssd_xwalk[["permco", "entity", "dt_start", "dt_end"]]
    permco_idrssd_xwalk["dt_end"] = pd.to_datetime(permco_idrssd_xwalk["dt_end"], errors="coerce", format="%Y%m%d")
    permco_idrssd_xwalk["dt_start"] = pd.to_datetime(permco_idrssd_xwalk["dt_start"], errors="coerce", format="%Y%m%d")
    permco_idrssd_xwalk.rename(columns={"entity": "top_parent_idrssd"}, inplace=True)

    # ------------------------------------------------------------------
    # 1) WRITE UNIQUE PERMCOs TO permco_codes.txt (FOR WRDS QUERY)
    # ------------------------------------------------------------------
    permcos = permco_idrssd_xwalk["permco"].dropna().astype(int).unique()

    if write_txt:
        with open(f"{path_wrds}/permco_codes.txt", "w") as f:
            for permco in permcos:
                f.write(f"{permco}\n")

    # Read WRDS export
    wrds_data = pd.read_csv(os.path.join(path_wrds, 'wrds_data.csv'))

    # ------------------------------------------------------------------
    # 2) PROCESS WRDS DATA
    # ------------------------------------------------------------------
    
    # Column names to lowercase
    wrds_data.columns = [col.lower() for col in wrds_data.columns]

    # Rename lpermco->permco, lpermno->permno, datacqtr->date
    wrds_data.rename(columns={'lpermco': 'permco',
                              'lpermno': 'permno',
                              'datacqtr': 'date',
                              }, inplace=True)

    # Convert date to datetime and keep from 2001 onwards
    wrds_data["date"] = wrds_data["date"].astype(str)
    #wrds_data["date"] = pd.to_datetime(wrds_data["date"], errors="coerce")
    wrds_data["date"] = pd.PeriodIndex(wrds_data["date"], freq="Q").end_time.normalize()
    
    #wrds_data["date"] = pd.PeriodIndex(wrds_data["date"], freq="Q").end_time.normalize()
    wrds_data = wrds_data[wrds_data["date"].dt.year > 2000]

    # Keep only relevant columns
    wrds_data = wrds_data[["date", "permco", "permno", "tic"]]

    # Merge WRDS data with crosswalk on permco to add 'entity'
    dt = wrds_data.merge(permco_idrssd_xwalk, on="permco").query("dt_start <= date <= dt_end")

    return dt

def find_child_at_date(df_relationship, top_parent_idrssd, date, verbose=False):
    """
    Return the set of children for a given top_parent_idrssd on a given date.
    Assumes df_relationship is indexed by 'id_rssd_parent' as in your setup.
    Parameters
    ----------
    df_relationship : pandas.DataFrame (indexed by 'id_rssd_parent')
    top_parent_idrssd : int
    date : str or pandas.Timestamp
    verbose : bool, default False
        If True, print debugging info.
    Returns
    -------
    set[int]
        All unique children of `top_parent_idrssd` active on `date`.
        
    """
    d = pd.to_datetime(date, errors="coerce")
    # --- filter df_relationship to links ACTIVE on that date for that parent ---
    sub = df_relationship.loc[int(top_parent_idrssd)]       # DataFrame if multiple rows, Series if single
    
    if isinstance(sub, pd.Series):                          # normalize to DataFrame
        sub = sub.to_frame().T

    mask = (sub["start_rel_date"] <= d) & (d <= sub["end_rel_date"])
    children = sub.loc[mask, "id_rssd_offspring"].dropna().astype(int).tolist()

    if verbose:
        print(f"{top_parent_idrssd=}  {d.date()=}")
        print(f"#children: {sorted(children)}")

    return set(children)


def find_descendants_at_date(
        df_relationship,
        top_parent_idrssd:  int, 
        fdic_cert_filter:   set,
        date
        ):
    """
    Return the full set of descendants (children, grandchildren, ... )
    for a given top_parent_idrssd on a given date, using the existing
    `find_child_at_date(df_relationship, top_parent_idrssd, date)` function.

    - Uses a BFS over parents at the same `date`.
    - Avoids cycles/duplicates via a `visited` set.
    - Assumes `df_relationship` is indexed by 'id_rssd_parent' as in your setup.

    Parameters
    ----------
    df_relationship : pandas.DataFrame (indexed by 'id_rssd_parent')
    top_parent_idrssd : int
    date : str or pandas.Timestamp

    Returns
    -------
    set[int]
        All unique descendants of `top_parent_idrssd` active on `date`.
    """
    d = pd.to_datetime(date, errors="coerce")
    if pd.isna(d):
        return set()

    # Initialize sets. 
    descendants = set()
    # visited tracks all nodes we've already expanded, including the root to avoid self-inclusion.
    visited = set([top_parent_idrssd])  # track nodes we've already expanded

    # seed with the root's children (if root is present as a parent)
    frontier = []
    if int(top_parent_idrssd) in df_relationship.index:
        # find first generation children
        first_kids = find_child_at_date(df_relationship, top_parent_idrssd, d)
        # add them to descendants, visited, and frontier
        descendants |= first_kids
        visited |= first_kids
        frontier.extend(first_kids)

    # BFS over generations
    while frontier:
        current = frontier.pop()
        # only expand nodes that appear as parents
        if int(current) not in df_relationship.index:
            continue

        kids = find_child_at_date(df_relationship, current, d)
        new = kids - visited
        if not new:
            continue

        descendants |= new
        visited |= new
        frontier.extend(new)

        """
        A small example of the frontier object:
        1) start: frontier = {c1, c2}
        2) pop c2 → finds {g3, g4} → frontier = {c1, g3, g4}
        3) pop g4 → finds {g5} → frontier = {c1, g3, g5}
        4) ... repeat until frontier is empty (no nodes left to expand)
        """

    return visited & fdic_cert_filter

def create_tic_parent_df(path):
    """
    Create a DataFrame mapping each ticker to its parent entity.
    The resulting DataFrame has columns:
        - date (Timestamp)
        - top_parent_idrssd (int)
        - child_idrssd (int)
        - permco (int)
        - tic (str)

    The key steps are:
    - Read and process the relationships data to build a parent→offspring mapping.
    - Merge this mapping with the ticker DataFrame to associate each child with its parent's ticker information.
    - Filter out rows where the ticker is missing.

    Key variables and functions:
    - df_tickers: DataFrame with columns ['date', 'top_parent_idrssd', 'permco', 'tic']
    - df_relationship: DataFrame with parent-child relationships and active dates.
    - find_descendants_at_date: Function to find all descendants of a parent at a given date.
    - df_family: DataFrame mapping each (top_parent_idrssd, date) to all its descendants.
    - df_merged: Final merged DataFrame with tickers for each child bank.

    Parameters
    ----------
    path : str
        Base path containing the 'ffiec/extracted/nic' and 'wrds_compustat' subfolders.

    Returns
    -------
    pd.DataFrame

    """

    # Give the path for the raw data folders, define path to subfolders
    nic_folder = os.path.join(path, "ffiec", "extracted", "nic")
    path_wrds = os.path.join(path, "wrds_compustat")

    # ------------------------------------------------------------------------
    # Ticker dataframe
    # ------------------------------------------------------------------------
    # Create ticker DataFrame, format columns
    df_tickers = create_ticker_df(path_wrds)
    df_tickers.rename(columns={'entity': 'top_parent_idrssd'}, inplace=True)

    # ------------------------------------------------------------------------
    # Relationships dataframe
    # ------------------------------------------------------------------------
    # Read relationships data, format columns
    df_relationship = pd.read_csv(os.path.join(nic_folder, "CSV_RELATIONSHIPS.csv"))
    df_relationship.columns = df_relationship.columns.str.replace("#", "")
    df_relationship.columns = [col.lower() for col in df_relationship.columns]
    df_relationship = df_relationship[["id_rssd_parent", "id_rssd_offspring", "d_dt_start", "d_dt_end"]]
    df_relationship.rename(columns={
        "d_dt_start": "start_rel_date",
        "d_dt_end": "end_rel_date",
    }, inplace=True)

    df_relationship['start_rel_date'] = pd.to_datetime(df_relationship['start_rel_date'], errors='coerce')
    df_relationship['end_rel_date'] = pd.to_datetime(df_relationship['end_rel_date'], errors='coerce')

    # fill NaT with a far future date
    df_relationship['end_rel_date'] = df_relationship['end_rel_date'].fillna(pd.Timestamp("2100-12-31"))
    df_relationship.set_index('id_rssd_parent', inplace=True)


    # ------------------------------------------------------------------------
    # Attributes dataframe
    # ------------------------------------------------------------------------
    active_fp = os.path.join(nic_folder, "CSV_ATTRIBUTES_ACTIVE.CSV")
    closed_fp = os.path.join(nic_folder, "CSV_ATTRIBUTES_CLOSED.CSV")

    # Read attributes: keep only the RSSD and charter code columns
    active = pd.read_csv(active_fp, usecols=["#ID_RSSD", "ID_FDIC_CERT"], low_memory=False)
    closed = pd.read_csv(closed_fp, usecols=["#ID_RSSD", "ID_FDIC_CERT"], low_memory=False)

    # Combine, standardize, and de-duplicate by idrssd
    attrs = pd.concat([active, closed], ignore_index=True).drop_duplicates()

    attrs.columns = [col.lower() for col in attrs.columns]
    attrs.rename(columns={"#id_rssd": "id_rssd"}, inplace=True)

    # Get the ids of banks with an fdic_cert.
    fdic_cert_filter = set(attrs.loc[attrs["id_fdic_cert"] > 0, "id_rssd"].astype(int))


    # ------------------------------------------------------------------------
    # Create "df_family": maps each (top_parent_idrssd, date) to all its descendants
    # ------------------------------------------------------------------------
    all_top_parents = df_tickers['top_parent_idrssd'].unique()
    all_unique_dates = df_tickers['date'].unique()

    records = []

    for pid in all_top_parents:
        for d in all_unique_dates:
            # get descendants (children, grandchildren, ...) at this date for this parent
            family = find_descendants_at_date(df_relationship, pid, fdic_cert_filter, d)
            if not family:
                continue
            # append one row per child
            d_ts = pd.to_datetime(d, errors="coerce")
            for k in sorted(family):
                records.append({
                    "date": d_ts,                 # keep as Timestamp for easy merging/filters
                    "top_parent_idrssd": int(pid),
                    "child_idrssd": int(k),
                })

    # Build final DataFrame
    df_family = (pd.DataFrame.from_records(records)
                    .drop_duplicates()
                    .sort_values(["date", "top_parent_idrssd", "child_idrssd"])
                    .reset_index(drop=True))

    # merge df_tickers with df_family to get tickers for top parents:
    df_merged = pd.merge(
        df_family,
        df_tickers[['date', 'top_parent_idrssd', 'permco', 'tic']],
        on=['date', 'top_parent_idrssd'],
        how='left'
    )

    # drop the rows in which "tic" is missing
    df_merged = df_merged[~df_merged["tic"].isna()]



    return df_merged

def binned_scatter(
    x,
    y,
    q,
    marker="o",
    dispersion=False,
    label=None,
    color='navy',
    x_axis="rank",     # "rank"  → percentile ranks    (default, original behaviour)
                       # "value" → actual x-values
    alpha=1.0
):
    """
    Scatter the mean of *y* in q-quantile bins of *x*.

    Parameters
    ----------
    x, y : array-like or pd.Series
    q    : int
        Number of equal-frequency bins.
    marker : str
        Matplotlib marker for the mean dots.
    dispersion : bool
        If True, also plot the median and IQR of *y* in each bin.
    label : str | None
        Legend label for the mean dots.
    x_axis : {"rank", "value"}
        What to place on the x-axis:
        - "rank"  → percentile ranks of *x* (0–1).
        - "value" → the underlying *x* (in data units).
    """

    # -- ensure pandas Series -------------------------------------------------
    if not isinstance(x, pd.Series):
        x = pd.Series(x, name=getattr(x, "name", None))
    if not isinstance(y, pd.Series):
        y = pd.Series(y, name=getattr(y, "name", None))

    # -- percentile ranks & bin membership -----------------------------------
    x_pct = x.rank(method="average", pct=True)
    x_binned = pd.qcut(x_pct, q=q, duplicates="drop")

    # -- within-bin statistics ------------------------------------------------
    bin_centers, means, medians, mins, maxs = [], [], [], [], []

    for interval in x_binned.unique():
        mask = x_binned == interval
        # centre depends on the chosen x-axis
        if x_axis == "rank":
            bin_center = x_pct[mask].mean()
        elif x_axis == "value":
            bin_center = x[mask].mean()
        else:
            raise ValueError("x_axis must be 'rank' or 'value'.")

        ys = y[mask]
        bin_centers.append(bin_center)
        means.append(ys.mean())
        medians.append(ys.median())
        mins.append(ys.quantile(0.25))
        maxs.append(ys.quantile(0.75))

    # -- sort by x ------------------------------------------------------------
    order = np.argsort(bin_centers)
    bin_centers = np.array(bin_centers)[order]
    means       = np.array(means)[order]
    medians     = np.array(medians)[order]
    mins        = np.array(mins)[order]
    maxs        = np.array(maxs)[order]

    # -- plot -----------------------------------------------------------------
    plt.scatter(
        bin_centers,
        means,
        marker=marker,
        alpha=alpha,
        s=50,
        edgecolors="black",
        color=color,
        label=label,
    )

    if dispersion:
        plt.scatter(bin_centers, medians, marker=marker, s=50, alpha=0.7, color="green")
        plt.scatter(bin_centers, mins,    marker=marker, s=50, alpha=0.7, color="grey")
        plt.scatter(bin_centers, maxs,    marker=marker, s=50, alpha=0.7, color="grey")

    # -- labels & grid --------------------------------------------------------
    if x_axis == "rank":
        plt.xlabel(f"Percentile Rank of {x.name or 'x'}")
        ticks = np.linspace(0, 1, 6)
        plt.xticks(ticks, [f"{int(t*100)}" for t in ticks])
    else:  # actual values
        plt.xlabel(x.name or "x")

    plt.ylabel(y.name or "y")
    plt.grid(True, linestyle="--", alpha=0.5, linewidth=0.5, color="lightgrey")
