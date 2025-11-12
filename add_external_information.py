import pandas as pd
import os

from aux_functions import *

def add_external_data_attributes(path: str, df: pd.DataFrame) -> pd.DataFrame:
    """
    Enrich a Call Reports DataFrame with bank charter information, resolving M&A chains to the **final successor**.

    ---------------------------------------------------------------------
    WHAT THIS DOES (high level)
    ---------------------------------------------------------------------
    1) Reads NIC attributes (active + closed) with columns:
          - '#ID_RSSD' (bank id)
          - 'CHTR_TYPE_CD' (charter type; e.g., numeric codes like 200, 250, 300)
    2) Merges charter onto your DataFrame `df` by 'idrssd'.
    3) For rows still missing a charter, follows M&A links from:
          '#ID_RSSD_PREDECESSOR'  →  'ID_RSSD_SUCCESSOR'
       repeatedly (predecessor → successor → successor → ...) until the **final successor**
       that has no further successor. It then assigns the **final successor's charter**
       back to the original predecessor.

    ---------------------------------------------------------------------
    REQUIRED INPUT FILES (exact columns)
    ---------------------------------------------------------------------
    - CSV_ATTRIBUTES_ACTIVE.CSV: columns ['#ID_RSSD', 'CHTR_TYPE_CD']
    - CSV_ATTRIBUTES_CLOSED.CSV: columns ['#ID_RSSD', 'CHTR_TYPE_CD']
    - CSV_TRANSFORMATIONS.CSV:  columns ['#ID_RSSD_PREDECESSOR', 'ID_RSSD_SUCCESSOR']

    ---------------------------------------------------------------------
    MINI EXAMPLE (numeric charter codes)
    ---------------------------------------------------------------------
    Suppose your working df has banks: idrssd = {1, 2, 3, 11, 12}

    Attributes (after combining active + closed):
        idrssd  CHTR_TYPE_CD
        ------  ------------
          11        200
          12        250
           3        300

    Transformations (predecessor → successor):
        pred  succ
        ----  ----
          1     2
          2    11
         11    12

    • Direct merge gives charters for 3 (=300), 11 (=200), 12 (=250). Banks 1 and 2 are missing.
    • Walk M&A chains to the final successor:
        final_successor(1): 1 → 2 → 11 → 12     ⇒ 12
        final_successor(2): 2 → 11 → 12         ⇒ 12
        final_successor(3): 3                   ⇒  3
        final_successor(11): 11 → 12            ⇒ 12
        final_successor(12): 12                 ⇒ 12
    • Final successors’ charters (via a lookup) are numeric:
        12 → 250, 3 → 300, 11 → 200
    • Therefore, banks 1 and 2 inherit the charter **250** from their final successor 12.

    ---------------------------------------------------------------------
    KEY OBJECTS IN THE CODE (starting from charter_lookup)
    ---------------------------------------------------------------------
    - charter_lookup = attrs.set_index("idrssd")["CHTR_TYPE_CD"]
        A pandas Series mapping idrssd → charter (numeric), e.g.
            11 → 200, 12 → 250, 3 → 300

    - final_successor(start_id)
        Follows succ_map (predecessor→successor dict) until no successor remains.
        Examples:
            final_successor(1) = 12
            final_successor(2) = 12
            final_successor(3) =  3

    - final_succ = pd.Series({i: final_successor(i) for i in need_ids})
        A Series whose INDEX is the set of original ids missing a charter,
        and whose VALUES are the corresponding final successor ids.
        Example:
            final_succ
            1    12
            2    12
            dtype: int64

        Then:
            fill_charter = final_succ.map(charter_lookup)
        converts successor ids to their numeric charter codes, preserving the original
        ids as the index:
            fill_charter
            1    250
            2    250
            dtype: int64 (or Int64)

    ---------------------------------------------------------------------
    IMPORTANT NOTE
    ---------------------------------------------------------------------
    - In pandas, when combining boolean masks, use "&" (bitwise AND), not "and".
      We use:
          missing_mask = df["charter_type"].isna() & df["idrssd"].notna()

    Parameters
    ----------
    path : str
        Directory containing the three CSV files above.
    df : pd.DataFrame
        A DataFrame that contains an 'idrssd' column. This function will add
        a column 'charter_type' with charter codes.

    Returns
    -------
    pd.DataFrame
        A copy of `df` with a new 'charter_type' column filled either directly
        from attributes or (when missing) inherited from the final successor.
    """

    # ------------------------------------------------------------------
    # 1) READ & PREP ATTRIBUTES (ACTIVE + CLOSED)
    # ------------------------------------------------------------------

    # Build full paths for attributes CSVs
    active_fp = os.path.join(path, "CSV_ATTRIBUTES_ACTIVE.CSV")
    closed_fp = os.path.join(path, "CSV_ATTRIBUTES_CLOSED.CSV")

    # Read attributes: keep only the RSSD and charter code columns
    active = pd.read_csv(active_fp, usecols=["#ID_RSSD", "CHTR_TYPE_CD"], low_memory=False)
    closed = pd.read_csv(closed_fp, usecols=["#ID_RSSD", "CHTR_TYPE_CD"], low_memory=False)

    # Combine, standardize, and de-duplicate by idrssd
    attrs = pd.concat([active, closed], ignore_index=True)
    attrs = attrs.rename(columns={"#ID_RSSD": "idrssd"})
    attrs = attrs.dropna(subset=["idrssd"])
    attrs = attrs.drop_duplicates(subset=["idrssd"], keep="last")
    attrs["idrssd"] = pd.to_numeric(attrs["idrssd"], errors="coerce").astype("Int64")

    # ------------------------------------------------------------------
    # 2) MERGE ATTRIBUTES INTO THE INPUT DF
    # ------------------------------------------------------------------

    #! Work directly on df, so as to not create a new copy.
    if "idrssd" not in df.columns:
        raise ValueError("Input df must contain an 'idrssd' column.")
    df["idrssd"] = pd.to_numeric(df["idrssd"], errors="coerce").astype("Int64")

    # Merge charter code directly; call the merged column 'charter_type'
    df = df.merge(
        attrs.rename(columns={"CHTR_TYPE_CD": "charter_type"}),
        on="idrssd",
        how="left"
    )

    # Early exit: if nothing is missing, we're done
    if df["charter_type"].notna().all():
        return df

    # ------------------------------------------------------------------
    # 3) READ TRANSFORMATIONS (PREDECESSOR → SUCCESSOR)
    # ------------------------------------------------------------------

    # Path to transformations file; if absent, we cannot backfill via successors
    xfrm_fp = os.path.join(path, "CSV_TRANSFORMATIONS.CSV")
    if not os.path.isfile(xfrm_fp):
        return df

    # Read with fixed column names; rename to simple 'pred' and 'succ'
    x = pd.read_csv(
        xfrm_fp,
        usecols=["#ID_RSSD_PREDECESSOR", "ID_RSSD_SUCCESSOR"],
        low_memory=False
    ).rename(columns={
        "#ID_RSSD_PREDECESSOR": "pred",
        "ID_RSSD_SUCCESSOR": "succ"
    })

    # Type to nullable integers; remove invalid rows
    x["pred"] = pd.to_numeric(x["pred"], errors="coerce").astype("Int64")
    x["succ"] = pd.to_numeric(x["succ"], errors="coerce").astype("Int64")
    x = x.dropna(subset=["pred", "succ"])

    # If multiple rows exist for the same predecessor, keep the last (most recent link)
    x = x.drop_duplicates(subset=["pred"], keep="last")

    # Guard against self-loops (a predecessor pointing to itself)
    x = x[x["pred"] != x["succ"]]

    # Build a fast lookup dict: predecessor → direct successor
    succ_map = dict(zip(x["pred"].astype("int64"), x["succ"].astype("int64")))

    # Build a Series to map idrssd → charter code (numeric)
    charter_lookup = attrs.set_index("idrssd")["CHTR_TYPE_CD"]

    # ------------------------------------------------------------------
    # 4) WALKER: FIND THE FINAL SUCCESSOR FOR A GIVEN START ID
    # ------------------------------------------------------------------

    def final_successor(start):
        """
        Follow predecessor→successor links until we reach a node with no successor.
        Returns the final successor id (or None if start is missing).
        """
        if pd.isna(start):
            return None
        cur = int(start)
        seen = set()  # prevents infinite loops if cycles exist
        while cur in succ_map and cur not in seen:
            seen.add(cur)
            cur = succ_map[cur]
        return cur

    # ------------------------------------------------------------------
    # 5) IDENTIFY MISSING CHARTERS & BACKFILL FROM FINAL SUCCESSORS
    # ------------------------------------------------------------------

    # Mask rows that lack charter but do have an idrssd
    missing_mask = df["charter_type"].isna() & df["idrssd"].notna()

    # Unique list of ids that need a charter fill
    need_ids = df.loc[missing_mask, "idrssd"].dropna().astype("int64").unique()

    # Series: index = original id needing fill, value = final successor id
    final_succ = pd.Series({i: final_successor(i) for i in need_ids})

    # Map successor ids → charter codes (numeric), keeping original ids as the index
    fill_charter = final_succ.map(charter_lookup)

    # Assign back only where charter is missing
    df.loc[missing_mask, "charter_type"] = df.loc[missing_mask, "idrssd"].map(fill_charter)

    # ------------------------------------------------------------------
    # 6) RETURN THE ENRICHED DATAFRAME
    # ------------------------------------------------------------------

    return df


def add_external_data_tic(path: str, df: pd.DataFrame) -> pd.DataFrame:

    """
    Enrich a Call Reports DataFrame with bank holding company information,
    by merging in the columns 'tic' and 'top_parent_idrssd' from the NIC. 

    Parameters
    ----------
    path : str
        Path to the "raw" data directory that contains the NIC files and the CRSP crosswalk.
    df : pd.DataFrame
        A DataFrame that contains an 'idrssd' column.
    Returns
    -------
    pd.DataFrame
        A copy of `df` with new columns 'tic', 'top_parent_idrssd', 'permco' merged in.
    """

    # use the path to get the tic and parent data
    df_tic_parent = create_tic_parent_df(path)

    # ! (Avoid creating a new copy of the dataset) merge the tic and parent data to the df:
    df = pd.merge(df, df_tic_parent,
                        how='left',
                        left_on=['date', 'idrssd'],
                        right_on=['date', 'child_idrssd']
                        ).drop(columns=['child_idrssd'])
    
    return df