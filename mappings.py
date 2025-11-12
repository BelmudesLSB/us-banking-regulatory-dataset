mappings = [
    # ============================================================================================================
    # ================================ Schedule RC - Balance Sheet Variables =====================================
    # ============================================================================================================
    #? ------------------------------------------- ASSETS --------------------------------------------------
    # Create 'total_assets' from rcon2170 and rcfd2170:
    {
        "new_var":      "total_assets",     # End of quarter, in thousand of dollars
        "first_col":    "rcon2170",
        "second_col":   "rcfd2170",
        "method":       "first",
    }, 
    # * ----------------------------------------------------------------------------------------------------------
    # 1a) Create 'currency_and_coin' from rcon0081 and rcfd0081:
    {
        "new_var":      "currency_and_coin", # End of quarter, in thousand of dollars
        "first_col":    "rcon0081",
        "second_col":   "rcfd0081",
        "method":       "first",
    },
    # Includes:
    # US currency and coin.
    # Noninterest-bearing demand deposit balances at other depository institutions.
    # * ----------------------------------------------------------------------------------------------------------
    # 1b) Create 'int_bearing_balances' from rcon0071 and rcfd0071:
    {
        "new_var":      "int_bearing_balances", # End of quarter, in thousand of dollars
        "first_col":    "rcon0071",
        "second_col":   "rcfd0071",
        "method":       "first",
    },
    # Includes:
    # - Interest-bearing accounts at the Federal Reserve (Reserves).
    # - Certain foreign deposits.
    # * ----------------------------------------------------------------------------------------------------------
    # 1.1) Create 'cash2' from 'currency_and_coin' and 'int_bearing_balances':
    {
        "new_var":      "cash2",            # End of quarter, in thousand of dollars
        "first_col":    "currency_and_coin",
        "second_col":   "int_bearing_balances",
        "method":       "sum",
    },
    # * ----------------------------------------------------------------------------------------------------------
    # 1.2) Create 'cash1' from rcon0010 and rcfd0010:
    {
        "new_var":      "cash1",            # End of quarter, in thousand of dollars
        "first_col":    "rcon0010",
        "second_col":   "rcfd0010",
        "method":       "first",
    },
    # * ----------------------------------------------------------------------------------------------------------
    # 1.3) Create 'cash' from 'cash1' and 'cash2':
    {
        "new_var":      "cash",            # End of quarter, in thousand of dollars
        "first_col":    "cash1",
        "second_col":   "cash2",
        "method":       "first",
    },
    # We follow the definition of Dreschler et. al (2021) to construct our definition of cash. 
    # * ----------------------------------------------------------------------------------------------------------
    # 2a) Create 'securities_htm_ac' from rcon1754 and rcfd1754 (before 2019-03-31) and rconjj34 and rcfdjj34 (after 2019-03-31):
    {
        "new_var":          "securities_htm_ac", # End of quarter, in thousand of dollars
        "first_col":        "rcon1754",
        "second_col":       "rcfd1754",
        "method":           "first",
    },
    # Includes:
    # - Securities held to maturity (HTM) are debt securities that the bank intends to hold until maturity.
    # - HTM securities are reported at amortized cost, not fair value.
    # Remark:
    # - An example of "Amortized Cost Accounting" can be found in the README file of the repository.
    # - From 2019-03-31 onwards, the variables rcon1754 and rcfd1754 started being reported only in the RC-B schedule, and the balance sheet
    #   variables rconjj34 and rcfdjj34 were introduced to replace them. Those are net of Allowance for Credit Losses (ACL), that can be found under
    #   riadjh90.
    #! ADD ALL THE ACL VARIABLES TO THE MAPPINGS FILE WHEN YOU REACH THE RI-SCHEDULE.
    # * ----------------------------------------------------------------------------------------------------------
    # 2b) Create 'securities_afs_fv' from rcon1773 and rcfd1773:
    {
        "new_var":      "securities_afs_fv",  # End of quarter, in thousand of dollars
        "first_col":    "rcon1773",
        "second_col":   "rcfd1773",
        "method":       "first",
    },
    # Includes:
    # - Securities available for sale (AFS) are debt securities that the bank may sell before maturity.
    # - AFS securities are reported at fair value, with unrealized gains and losses recorded in other comprehensive income (OCI).
    # Remark:
    # - The ACL for AFS securities is reported under riadjh96, but it is not included in the securities_afs variable.
    # * ----------------------------------------------------------------------------------------------------------
    # 2c) Create 'securities_equity' from rconja22 and rcfdja22:
    {
        "new_var":      "securities_equity", # End of quarter, in thousand of dollars
        "first_col":    "rconja22",
        "second_col":   "rcfdja22",
        "method":       "first",
    },
    # Includes:
    # - Equity securities are stocks or other equity interests in other companies (not hold for trading).
    # - They are reported at fair value, with unrealized gains and losses recorded in other comprehensive income (OCI).
    # * ----------------------------------------------------------------------------------------------------------
    # 3a) Create 'ff_sold' from rconb987:
    {
        "new_var":      "ff_sold",         # End of quarter, in thousand of dollars
        "first_col":    "rconb987",
        "method":       "rename",
    },
    # Includes:
    # - Unsecured, short-term loans of excess reserves to other US depository institutions.
    # - Usually overnigh and interest earning.
    # * ----------------------------------------------------------------------------------------------------------
    # 3b) Create 'repo_asset' from rconb989 and rcfdb989:
    {
        "new_var":      "repo_asset",     # End of quarter, in thousand of dollars
        "first_col":    "rconb989",
        "second_col":   "rcfdb989",
        "method":       "first",
    },
    # Includes:
    # Short term agreements to buy securities and resell them at a later date at a fixed price.
    # * ----------------------------------------------------------------------------------------------------------
    # 4) Define 'total_loans' from rcon2122 and rcfd2122:
    {
        "new_var":      "total_loans",    # End of quarter, in thousand of dollars
        "first_col":    "rcon2122",
        "second_col":   "rcfd2122",
        "method":       "first",
    },
    # * ----------------------------------------------------------------------------------------------------------
    #? ------------------------------------------- LIABILITIES ---------------------------------------------------
    # * ----------------------------------------------------------------------------------------------------------
    # 13) Create 'total_deposits' from rcon2200 and rcfd2200:
    {
        "new_var":      "total_deposits",  # End of quarter, in thousand of dollars
        "first_col":    "rcon2200",
        "method":       "rename",
    },
    # * ----------------------------------------------------------------------------------------------------------
    # 14a) Create 'ff_purchased' from rconbb93:
    {
        "new_var":      "ff_purchased",  # End of quarter, in thousand of dollars
        "first_col":    "rconb993",
        "method":       "rename",
    },
    # * ----------------------------------------------------------------------------------------------------------
    # 14b) Create 'repo_debt' from rconb995 and rcfdb995:
    {
        "new_var":      "repo_debt",  # End of quarter, in thousand of dollars
        "first_col":    "rconb995",
        "second_col":   "rcfdb995",
        "method":       "first",
    },
    # * ----------------------------------------------------------------------------------------------------------
    # 16) Create 'sub_notes_debentures' from rcon3200 and rcfd3200:
    {
        "new_var":      "sub_notes_debentures",  # End of quarter, in thousand of dollars
        "first_col":    "rcon3200",
        "second_col":   "rcfd3200",
        "method":       "first",
    }, 
    # * ----------------------------------------------------------------------------------------------------------
    # Create 'total_liabilities' from rcon29448 and rcfd29448:
    {
        "new_var":      "total_liabilities",  # End of quarter, in thousand of dollars
        "first_col":    "rcon2948",
        "second_col":   "rcfd2948",
        "method":       "first",
    },
    # * ----------------------------------------------------------------------------------------------------------
    #? --------------------------------------------- EQUITY ------------------------------------------------------
    # * ----------------------------------------------------------------------------------------------------------
    # 23) Create 'preferred_stock' from rcon3838 and rcfd3838:
    {
        "new_var":      "preferred_stock",  # End of quarter, in thousand of dollars
        "first_col":    "rcon3838",
        "second_col":   "rcfd3838",
        "method":       "first",
    },
    # * ----------------------------------------------------------------------------------------------------------
    # 24) Create 'common_stock' from rcon3230 and rcfd3230:
    {
        "new_var":      "common_stock",  # End of quarter, in thousand of dollars
        "first_col":    "rcon3230",
        "second_col":   "rcfd3230",
        "method":       "first",
    },
    # * ----------------------------------------------------------------------------------------------------------
    # Create 'book_value_stocks' from 'preferred_stock' and 'common_stock'
    {
        "new_var":      "book_value_stocks",  # End of quarter, in thousand of dollars
        "first_col":    "preferred_stock",
        "second_col":   "common_stock",
        "method":       "sum",
    },
    # * ----------------------------------------------------------------------------------------------------------
    # 25) Create 'stock_surplus' from rcon3839 and rcfd3839:
    {
        "new_var":      "stock_surplus",  # End of quarter, in thousand of dollars
        "first_col":    "rcon3839",
        "second_col":   "rcfd3839",
        "method":       "first",
    },
    # * ----------------------------------------------------------------------------------------------------------
    # 26a) Create 'retained_earnings' from rcon3632 and rcfd3632:
    {
        "new_var":      "retained_earnings",  # End of quarter, in thousand of dollars
        "first_col":    "rcon3632",
        "second_col":   "rcfd3632",
        "method":       "first",
    },
    # * ----------------------------------------------------------------------------------------------------------
    # 26b) Create 'aoci' from rconb530 and rcfdb530:
    {
        "new_var":      "aoci",  # End of quarter, in thousand of dollars
        "first_col":    "rconb530",
        "second_col":   "rcfdb530",
        "method":       "first",
    },
    # * ----------------------------------------------------------------------------------------------------------
    # create 'total_equity_capital' from rcon3210 and rcfd3210:
    {
        "new_var":      "total_equity_capital",  # End of quarter, in thousand of dollars
        "first_col":    "rcon3210",
        "second_col":   "rcfd3210",
        "method":       "first",
    },
    # ============================================================================================================
    # ================================= Schedule RC-B - Detailed Securities ======================================
    # ============================================================================================================
    #? ----------------------------------------- TREASURY SECURITIES ------------------------------------------
    # Create 'treasuries_htm_ac' from rcon0211 and rcfd0211:
    {
        "new_var":      "treasuries_htm_ac",  # End of quarter, in thousand of dollars
        "first_col":    "rcon0211",
        "second_col":   "rcfd0211",
        "method":       "first",
    }, 
    # * ----------------------------------------------------------------------------------------------------------
    # Create 'treasuries_htm_fv' from rcon0213 and rcfd0213:
    {
        "new_var":      "treasuries_htm_fv",  # End of quarter, in thousand of dollars
        "first_col":    "rcon0213",
        "second_col":   "rcfd0213",
        "method":       "first",
    },
    # * ----------------------------------------------------------------------------------------------------------
    # Create 'treasuries_afs_ac' from rcon1286 and rcfd1286:
    {
        "new_var":      "treasuries_afs_ac",  # End of quarter, in thousand of dollars
        "first_col":    "rcon1286",
        "second_col":   "rcfd1286",
        "method":       "first",
    },
    # * ----------------------------------------------------------------------------------------------------------
    # Create 'treasuries_afs_fv' from rcon1287 and rcfd1287:
    {
        "new_var":      "treasuries_afs_fv",  # End of quarter, in thousand of dollars
        "first_col":    "rcon1287",
        "second_col":   "rcfd1287",
        "method":       "first",
    },
    # * ----------------------------------------------------------------------------------------------------------
    # Create 'treasuries_ac' from 'treasuries_htm_ac' and 'treasuries_afs_ac':
    {
        "new_var":      "treasuries_ac",  # End of quarter, in thousand of dollars
        "first_col":    "treasuries_htm_ac",
        "second_col":   "treasuries_afs_ac",
        "method":       "sum",
    },
    # * ----------------------------------------------------------------------------------------------------------
    # Create 'treasuries_fv' from 'treasuries_htm_fv' and 'treasuries_afs_fv':
    {
        "new_var":      "treasuries_fv",  # End of quarter, in thousand of dollars
        "first_col":    "treasuries_htm_fv",
        "second_col":   "treasuries_afs_fv",
        "method":       "sum",
    },
    #? --------------------------------------- US GOV. AGENCY SECURITIES ---------------------------------------
    # Create 'rconht50_aux' from the sum of rcon1289 and rcon1294:
    {
        "new_var":      "rconht50_aux",  # End of quarter, in thousand of dollars
        "first_col":    "rcon1289",
        "second_col":   "rcon1294",
        "method":       "sum",
    },
    # Remark: this variable was interrupted on 2008-03-31 and replaced by the ht50 series.
    # * ----------------------------------------------------------------------------------------------------------
    # Create 'rcfdht50_aux' from the sum of rcfd1289 and rcfd1294:
    {
        "new_var":      "rcfdht50_aux",  # End of quarter, in thousand of dollars
        "first_col":    "rcfd1289",
        "second_col":   "rcfd1294",
        "method":       "sum",
    },
    # Remark: this variable was interrupted on 2008-03-31 and replaced by the ht50 series.
    # * ----------------------------------------------------------------------------------------------------------
    # Create 'agency_bonds_htm_ac' using the swicth_date of 2008-03-31:
    {
        "new_var":          "agency_bonds_htm_ac",  # End of quarter, in thousand of dollars
        "first_col":        "rconht50_aux",
        "second_col":       "rcfdht50_aux",
        "switch_date":      "2008-03-31",
        "first_col_post":   "rconht50",
        "second_col_post":  "rcfdht50",
        "method":           "first",
    },
    # * ----------------------------------------------------------------------------------------------------------
    # Create 'rconht51_aux' from the sum of rcon1290 and rcon1295:
    {
        "new_var":      "rconht51_aux",  # End of quarter, in thousand of dollars
        "first_col":    "rcon1290",
        "second_col":   "rcon1295",
        "method":       "sum",
    },
    # Remark: this variable was interrupted on 2008-03-31 and replaced by the ht51 series.
    # * ----------------------------------------------------------------------------------------------------------
    # Create 'rcfdht51_aux' from the sum of rcfd1290 and rcfd1295:
    {
        "new_var":      "rcfdht51_aux",  # End of quarter, in thousand of dollars
        "first_col":    "rcfd1290",
        "second_col":   "rcfd1295",
        "method":       "sum",
    },
    # Remark: this variable was interrupted on 2008-03-31 and replaced by the ht51 series.
    # * ----------------------------------------------------------------------------------------------------------
    # Create 'agency_bonds_htm_fv' using the swicth_date of 2008-03-31:
    {
        "new_var":          "agency_bonds_htm_fv",  # End of quarter, in thousand of dollars
        "first_col":        "rconht51_aux",
        "second_col":       "rcfdht51_aux",
        "switch_date":      "2008-03-31",
        "first_col_post":   "rconht51",
        "second_col_post":  "rcfdht51",
        "method":           "first",
    },
    # * ----------------------------------------------------------------------------------------------------------
    # Create 'rconht52_aux' from the sum of rcon1291 and rcon1297:
    {
        "new_var":      "rconht52_aux",  # End of quarter, in thousand of dollars
        "first_col":    "rcon1291",
        "second_col":   "rcon1297",
        "method":       "sum",
    },
    # Remark: this variable was interrupted on 2008-03-31 and replaced by the ht52 series.
    # * ----------------------------------------------------------------------------------------------------------
    # Create 'rcfdht52_aux' from the sum of rcfd1291 and rcfd1297:
    {
        "new_var":      "rcfdht52_aux",  # End of quarter, in thousand of dollars
        "first_col":    "rcfd1291",
        "second_col":   "rcfd1297",
        "method":       "sum",
    },
    # Remark: this variable was interrupted on 2008-03-31 and replaced by the ht52 series.
    # * ----------------------------------------------------------------------------------------------------------
    # Create 'agency_bonds_afs_ac' using the swicth_date of 2008-03-31:
    {
        "new_var":          "agency_bonds_afs_ac",  # End of quarter, in thousand of dollars
        "first_col":        "rconht52_aux",
        "second_col":       "rcfdht52_aux",
        "switch_date":      "2008-03-31",
        "first_col_post":   "rconht52",
        "second_col_post":  "rcfdht52",
        "method":           "first",
    },
    # * ----------------------------------------------------------------------------------------------------------
    # Create 'rconht53_aux' from the sum of rcon1293 and rcon1298:
    {
        "new_var":      "rconht53_aux",  # End of quarter, in thousand of dollars
        "first_col":    "rcon1293",
        "second_col":   "rcon1298",
        "method":       "sum",
    },
    # Remark: this variable was interrupted on 2008-03-31 and replaced by the ht53 series.
    # * ----------------------------------------------------------------------------------------------------------
    # Create 'rcfdht53_aux' from the sum of rcfd1293 and rcfd1298:
    {
        "new_var":      "rcfdht53_aux",  # End of quarter, in thousand of dollars
        "first_col":    "rcfd1293",
        "second_col":   "rcfd1298",
        "method":       "sum",
    },
    # Remark: this variable was interrupted on 2008-03-31 and replaced by the ht53 series.
    # * ----------------------------------------------------------------------------------------------------------
    # Create 'agency_bonds_afs_fv' using the swicth_date of 2008-03-31:
    {
        "new_var":          "agency_bonds_afs_fv",  # End of quarter, in thousand of dollars
        "first_col":        "rconht53_aux",
        "second_col":       "rcfdht53_aux",
        "switch_date":      "2008-03-31",
        "first_col_post":   "rconht53",
        "second_col_post":  "rcfdht53",
        "method":           "first",
    },
    # * ----------------------------------------------------------------------------------------------------------
    # Create 'agency_bonds_ac' from 'agency_bonds_htm_ac' and 'agency_bonds_afs_ac':
    {
        "new_var":      "agency_bonds_ac",  # End of quarter, in thousand of dollars
        "first_col":    "agency_bonds_htm_ac",
        "second_col":   "agency_bonds_afs_ac",
        "method":       "sum",
    },
    # * ----------------------------------------------------------------------------------------------------------
    # Create 'agency_bonds_fv' from 'agency_bonds_htm_fv' and 'agency_bonds_afs_fv':
    {
        "new_var":      "agency_bonds_fv",  # End of quarter, in thousand of dollars
        "first_col":    "agency_bonds_htm_fv",
        "second_col":   "agency_bonds_afs_fv",
        "method":       "sum",
    },
    #? ---------------------------------------------- STATE BONDS ----------------------------------------------
    # Create 'state_bonds_htm_ac' from rcon8496 and rcfd8496:
    {
        "new_var":      "state_bonds_htm_ac",  # End of quarter, in thousand of dollars
        "first_col":    "rcon8496",
        "second_col":   "rcfd8496",
        "method":       "first",
    },
    # * ----------------------------------------------------------------------------------------------------------
    # Create 'state_bonds_htm_fv' from rcon8497 and rcfd8497:
    {
        "new_var":      "state_bonds_htm_fv",  # End of quarter, in thousand of dollars
        "first_col":    "rcon8497",
        "second_col":   "rcfd8497",
        "method":       "first",
    },
    # * ----------------------------------------------------------------------------------------------------------
    # Create 'state_bonds_afs_ac' from rcon8498 and rcfd8498:
    {
        "new_var":      "state_bonds_afs_ac",  # End of quarter, in thousand of dollars
        "first_col":    "rcon8498",
        "second_col":   "rcfd8498",
        "method":       "first",
    },
    # * ----------------------------------------------------------------------------------------------------------
    # Create 'state_bonds_afs_fv' from rcon8499 and rcfd8499:
    {
        "new_var":      "state_bonds_afs_fv",  # End of quarter, in thousand of dollars
        "first_col":    "rcon8499",
        "second_col":   "rcfd8499",
        "method":       "first",
    },
    # * ----------------------------------------------------------------------------------------------------------
    # Create 'state_bonds_ac' from 'state_bonds_htm_ac' and 'state_bonds_afs_ac':
    {
        "new_var":      "state_bonds_ac",  # End of quarter, in thousand of dollars
        "first_col":    "state_bonds_htm_ac",
        "second_col":   "state_bonds_afs_ac",
        "method":       "sum",
    },
    # * ----------------------------------------------------------------------------------------------------------
    # Create 'state_bonds_fv' from 'state_bonds_htm_fv' and 'state_bonds_afs_fv':
    {
        "new_var":      "state_bonds_fv",  # End of quarter, in thousand of dollars
        "first_col":    "state_bonds_htm_fv",
        "second_col":   "state_bonds_afs_fv",
        "method":       "sum",
    },
    # * ----------------------------------------------------------------------------------------------------------
    #? --------------------------------------- MORTGAGE BACKED SECURITIES --------------------------------------
    # ---------------------------------------- RISKY MBS -------------------------------------------
    # Create 'mbs_risky_htm_ac_rcon' 
    {
        "new_var":      "mbs_risky_htm_ac_rcon",  # End of quarter, in thousand of dollars
        "first_col":    "rcon1709",
        "second_col":   "rcon1733",
        "method":       "sum",
        "switch_date":    "2011-03-31",
        "first_col_post": ("rcong308", "rcong320", "rconk146", "rconk154"),
    },
    # * ----------------------------------------------------------------------------------------------------------
    # Create 'mbs_risky_htm_ac_rcfd'
    {
        "new_var":      "mbs_risky_htm_ac_rcfd",  # End of quarter, in thousand of dollars
        "first_col":    "rcfd1709",
        "second_col":   "rcfd1733",
        "method":       "sum",
        "switch_date":    "2011-03-31",
        "first_col_post": ("rcfdg308", "rcfdg320", "rcfdk146", "rcfdk154"),
    },
    # * ----------------------------------------------------------------------------------------------------------
    # Aggregate 'mbs_risky_htm_ac' from 'mbs_risky_htm_ac_rcon' and 'mbs_risky_htm_ac_rcfd':
    {
        "new_var":      "mbs_risky_htm_ac",  # End of quarter, in thousand of dollars
        "first_col":    "mbs_risky_htm_ac_rcon",
        "second_col":   "mbs_risky_htm_ac_rcfd",
        "method":       "first",
    },
    # Remark: this series does not exist from 2009-06-30 to 2011-03-31.
    # * ----------------------------------------------------------------------------------------------------------
    # Create 'mbs_risky_htm_fv_rcon' 
    {
        "new_var":      "mbs_risky_htm_fv_rcon",  # End of quarter, in thousand of dollars
        "first_col":    "rcon1710",
        "second_col":   "rcon1734",
        "method":       "sum",
        "switch_date":    "2011-03-31",
        "first_col_post": ("rcong309", "rcong321", "rconk147", "rconk155"),
    },
    # * ----------------------------------------------------------------------------------------------------------
    # Create 'mbs_risky_htm_fv_rcfd'
    {
        "new_var":      "mbs_risky_htm_fv_rcfd",
        "first_col":    "rcfd1710",
        "second_col":   "rcfd1734",
        "method":       "sum",
        "switch_date":    "2011-03-31",
        "first_col_post": ("rcfdg309", "rcfdg321", "rcfdk147", "rcfdk155"),
    },
    # * ----------------------------------------------------------------------------------------------------------
    # Aggregate 'mbs_risky_htm_fv' from 'mbs_risky_htm_fv_rcon' and 'mbs_risky_htm_fv_rcfd':
    {
        "new_var":      "mbs_risky_htm_fv",  # End of quarter, in thousand of dollars
        "first_col":    "mbs_risky_htm_fv_rcon",
        "second_col":   "mbs_risky_htm_fv_rcfd",
        "method":       "first",
    },
    # Remark: this series does not exist from 2009-06-30 to 2011-03-31.
    # * ----------------------------------------------------------------------------------------------------------
    # Create 'mbs_risky_afs_ac_rcon' 
    {
        "new_var":      "mbs_risky_afs_ac_rcon",  # End of quarter, in thousand of dollars
        "first_col":    "rcon1711",
        "second_col":   "rcon1735",
        "method":       "sum",
        "switch_date":    "2011-03-31",
        "first_col_post": ("rcong310", "rcong322", "rconk148", "rconk156"),
    },
    # * ----------------------------------------------------------------------------------------------------------
    # Create 'mbs_risky_afs_ac_rcfd'
    {
        "new_var":      "mbs_risky_afs_ac_rcfd",  # End of quarter, in thousand of dollars
        "first_col":    "rcfd1711",
        "second_col":   "rcfd1735",
        "method":       "sum",
        "switch_date":    "2011-03-31",
        "first_col_post": ("rcfdg310", "rcfdg322", "rcfdk148", "rcfdk156"),
    },
    # * ----------------------------------------------------------------------------------------------------------
    # Aggregate 'mbs_risky_afs_ac' from 'mbs_risky_afs_ac_rcon' and 'mbs_risky_afs_ac_rcfd':
    {
        "new_var":      "mbs_risky_afs_ac",  # End of quarter, in thousand of dollars
        "first_col":    "mbs_risky_afs_ac_rcon",
        "second_col":   "mbs_risky_afs_ac_rcfd",
        "method":       "first",
    },
    # Remark: this series does not exist from 2009-06-30 to 2011-03-31.
    # * ----------------------------------------------------------------------------------------------------------
    # Create 'mbs_risky_afs_fv_rcon' 
    {
        "new_var":      "mbs_risky_afs_fv_rcon",  # End of quarter, in thousand of dollars
        "first_col":    "rcon1713",
        "second_col":   "rcon1736",
        "method":       "sum",
        "switch_date":    "2011-03-31",
        "first_col_post": ("rcong311", "rcong323", "rconk149", "rconk157"),
    },
    # * ----------------------------------------------------------------------------------------------------------
    # Create 'mbs_risky_afs_fv_rcfd'
    {
        "new_var":      "mbs_risky_afs_fv_rcfd",
        "first_col":    "rcfd1713",
        "second_col":   "rcfd1736",
        "method":       "sum",
        "switch_date":    "2011-03-31",
        "first_col_post": ("rcfdg311", "rcfdg323", "rcfdk149", "rcfdk157"),
    },
    # * ----------------------------------------------------------------------------------------------------------
    # Aggregate 'mbs_risky_afs_fv' from 'mbs_risky_afs_fv_rcon' and 'mbs_risky_afs_fv_rcfd':
    {
        "new_var":      "mbs_risky_afs_fv",  # End of quarter, in thousand of dollars
        "first_col":    "mbs_risky_afs_fv_rcon",
        "second_col":   "mbs_risky_afs_fv_rcfd",
        "method":       "first",
    },
    # Remark: this series does not exist from 2009-06-30 to 2011-03-31.
    # * ----------------------------------------------------------------------------------------------------------
    # Create 'total_mbs_risky' from 'mbs_risky_htm_ac' and 'mbs_risky_afs_fv':
    {
        "new_var":      "total_mbs_risky",  # End of quarter, in thousand of dollars
        "first_col":    "mbs_risky_htm_ac",
        "second_col":   "mbs_risky_afs_fv",
        "method":       "sum",
    },
    # Remark: this series does not exist from 2009-06-30 to 2011-03-31.
    # * ----------------------------------------------------------------------------------------------------------
    # Create 'total_mbs_risky_ac' from 'mbs_risky_htm_ac' and 'mbs_risky_afs_ac':
    {
        "new_var":      "total_mbs_risky_ac",  # End of quarter, in thousand of dollars
        "first_col":    "mbs_risky_htm_ac",
        "second_col":   "mbs_risky_afs_ac",
        "method":       "sum",
    },
    # Remark: this series does not exist from 2009-06-30 to 2011-03-31.
    # * ----------------------------------------------------------------------------------------------------------
    # Create 'total_mbs_risky_fv' from 'mbs_risky_htm_fv' and 'mbs_risky_afs_fv':
    {
        "new_var":      "total_mbs_risky_fv",  # End of quarter, in thousand of dollars
        "first_col":    "mbs_risky_htm_fv",
        "second_col":   "mbs_risky_afs_fv",
        "method":       "sum",
    },
    # Remark: this series does not exist from 2009-06-30 to 2011-03-31.
    # * ----------------------------------------------------------------------------------------------------------
    # ---------------------------------------- SAFE MBS -------------------------------------------
    # Create 'mbs_safe_htm_ac_rcon' 
    {
        "new_var":      "mbs_safe_htm_ac_rcon",  # End of quarter, in thousand of dollars
        "first_col":    ("rcon1698", "rcon1703", "rcon1714", "rcon1718"),
        "switch_date":    "2011-03-31",
        "first_col_post": ("rcong300", "rcong304", "rcong312", "rcong316", "rconk142", "rconk150"),
        "method":       "sum",
    },
    # * ----------------------------------------------------------------------------------------------------------
    # Create 'mbs_safe_htm_ac_rcfd'
    {
        "new_var":      "mbs_safe_htm_ac_rcfd",  # End of quarter, in thousand of dollars
        "first_col":    ("rcfd1698", "rcfd1703", "rcfd1714", "rcfd1718"),
        "switch_date":    "2011-03-31",
        "first_col_post": ("rcfdg300", "rcfdg304", "rcfdg312", "rcfdg316", "rcfdk142", "rcfdk150"),
        "method":       "sum",
    },
    # * ----------------------------------------------------------------------------------------------------------
    # Aggregate 'mbs_safe_htm_ac' from 'mbs_safe_htm_ac_rcon' and 'mbs_safe_htm_ac_rcfd':
    {
        "new_var":      "mbs_safe_htm_ac",  # End of quarter, in thousand of dollars
        "first_col":    "mbs_safe_htm_ac_rcon",
        "second_col":   "mbs_safe_htm_ac_rcfd",
        "method":       "first",
    },
    # Remark: this series does not exist from 2009-06-30 to 2011-03-31.
    # * ----------------------------------------------------------------------------------------------------------
    # Create 'mbs_safe_htm_fv_rcon' 
    {
        "new_var":      "mbs_safe_htm_fv_rcon",  # End of quarter, in thousand of dollars
        "first_col":    ("rcon1699", "rcon1705", "rcon1715", "rcon1719"),
        "switch_date":    "2011-03-31",
        "first_col_post": ("rcong301", "rcong305", "rcong313", "rcong317", "rconk143", "rconk151"),
        "method":       "sum",
    },
    # * ----------------------------------------------------------------------------------------------------------
    # Create 'mbs_safe_htm_fv_rcfd'
    {
        "new_var":      "mbs_safe_htm_fv_rcfd",  # End of quarter, in thousand of dollars
        "first_col":    ("rcfd1699", "rcfd1705", "rcfd1715", "rcfd1719"),
        "switch_date":    "2011-03-31",
        "first_col_post": ("rcfdg301", "rcfdg305", "rcfdg313", "rcfdg317", "rcfdk143", "rcfdk151"),
        "method":       "sum",
    },
    # * ----------------------------------------------------------------------------------------------------------
    # Aggregate 'mbs_safe_htm_fv' from 'mbs_safe_htm_fv_rcon' and 'mbs_safe_htm_fv_rcfd':
    {
        "new_var":      "mbs_safe_htm_fv",  # End of quarter, in thousand of dollars
        "first_col":    "mbs_safe_htm_fv_rcon",
        "second_col":   "mbs_safe_htm_fv_rcfd",
        "method":       "first",
    },
    # Remark: this series does not exist from 2009-06-30 to 2011-03-31.
    # * ----------------------------------------------------------------------------------------------------------
    # Create 'mbs_safe_afs_ac_rcon' 
    {
        "new_var":      "mbs_safe_afs_ac_rcon",  # End of quarter, in thousand of dollars
        "first_col":    ("rcon1701", "rcon1706", "rcon1716", "rcon1731"),
        "switch_date":    "2011-03-31",
        "first_col_post": ("rcong302", "rcong306", "rcong314", "rcong318", "rconk144", "rconk152"),
        "method":       "sum",
    },
    # * ----------------------------------------------------------------------------------------------------------
    # Create 'mbs_safe_afs_ac_rcfd'
    {
        "new_var":      "mbs_safe_afs_ac_rcfd",  # End of quarter, in thousand of dollars
        "first_col":    ("rcfd1701", "rcfd1706", "rcfd1716", "rcfd1731"),
        "switch_date":    "2011-03-31",
        "first_col_post": ("rcfdg302", "rcfdg306", "rcfdg314", "rcfdg318", "rcfdk144", "rcfdk152"),
        "method":       "sum",
    },
    # * ----------------------------------------------------------------------------------------------------------
    # Aggregate 'mbs_safe_afs_ac' from 'mbs_safe_afs_ac_rcon' and 'mbs_safe_afs_ac_rcfd':
    {
        "new_var":      "mbs_safe_afs_ac",  # End of quarter, in thousand of dollars
        "first_col":    "mbs_safe_afs_ac_rcon",
        "second_col":   "mbs_safe_afs_ac_rcfd",
        "method":       "first",
    },
    # Remark: this series does not exist from 2009-06-30 to 2011-03-31.
    # * ----------------------------------------------------------------------------------------------------------
    # Create 'mbs_safe_afs_fv_rcon' 
    {
        "new_var":      "mbs_safe_afs_fv_rcon",  # End of quarter, in thousand of dollars
        "first_col":    ("rcon1702", "rcon1707", "rcon1717", "rcon1732"),
        "switch_date":    "2011-03-31",
        "first_col_post": ("rcong303", "rcong307", "rcong315", "rcong319", "rconk145", "rconk153"),
        "method":       "sum",
    },
    # * ----------------------------------------------------------------------------------------------------------
    # Create 'mbs_safe_afs_fv_rcfd'
    {
        "new_var":      "mbs_safe_afs_fv_rcfd",  # End of quarter, in thousand of dollars
        "first_col":    ("rcfd1702", "rcfd1707", "rcfd1717", "rcfd1732"),
        "switch_date":    "2011-03-31",
        "first_col_post": ("rcfdg303", "rcfdg307", "rcfdg315", "rcfdg319", "rcfdk145", "rcfdk153"),
        "method":       "sum",
    },
    # * ----------------------------------------------------------------------------------------------------------
    # Aggregate 'mbs_safe_afs_fv' from 'mbs_safe_afs_fv_rcon' and 'mbs_safe_afs_fv_rcfd':
    {
        "new_var":      "mbs_safe_afs_fv",  # End of quarter, in thousand of dollars
        "first_col":    "mbs_safe_afs_fv_rcon",
        "second_col":   "mbs_safe_afs_fv_rcfd",
        "method":       "first",
    },
    # Remark: this series does not exist from 2009-06-30 to 2011-03-31.
    # * ----------------------------------------------------------------------------------------------------------
    # Create 'total_mbs_safe' from 'mbs_safe_htm_ac' and 'mbs_safe_afs_fv':
    {
        "new_var":      "total_mbs_safe",  # End of quarter, in thousand of dollars
        "first_col":    "mbs_safe_htm_ac",
        "second_col":   "mbs_safe_afs_fv",
        "method":       "sum",
    },
    # Remark: this series does not exist from 2009-06-30 to 2011-03-31.
    # * ----------------------------------------------------------------------------------------------------------
    # Create 'total_mbs_safe_ac' from 'mbs_safe_htm_ac' and 'mbs_safe_afs_ac':
    {
        "new_var":      "total_mbs_safe_ac",  # End of quarter, in thousand of dollars
        "first_col":    "mbs_safe_htm_ac",
        "second_col":   "mbs_safe_afs_ac",
        "method":       "sum",
    },
    # Remark: this series does not exist from 2009-06-30 to 2011-03-31.
    # * ----------------------------------------------------------------------------------------------------------
    # Create 'total_mbs_safe_fv' from 'mbs_safe_htm_fv' and 'mbs_safe_afs_fv':
    {
        "new_var":      "total_mbs_safe_fv",  # End of quarter, in thousand of dollars
        "first_col":    "mbs_safe_htm_fv",
        "second_col":   "mbs_safe_afs_fv",
        "method":       "sum",
    },
    # Remark: this series does not exist from 2009-06-30 to 2011-03-31.
    # * ----------------------------------------------------------------------------------------------------------
    #? ----------------------------------------- AGGREGATE SECURITIES ------------------------------------------
    # Create 'securities_htm_fv' from rcon1771 and rcfd1771:
    {
        "new_var":      "securities_htm_fv",  # End of quarter, in thousand of dollars
        "first_col":    "rcon1771",
        "second_col":   "rcfd1771",
        "method":       "first",
    },
    # * ----------------------------------------------------------------------------------------------------------
    # Create 'securities_afs_ac' from rcon1772 and rcfd1772:
    {
        "new_var":      "securities_afs_ac",  # End of quarter, in thousand of dollars
        "first_col":    "rcon1772",
        "second_col":   "rcfd1772",
        "method":       "first",
    },
    # * ----------------------------------------------------------------------------------------------------------
    # Create 'securities_ac' from 'securities_htm' and 'securities_afs_ac':
    {
        "new_var":      "securities_ac",  # End of quarter, in thousand of dollars
        "first_col":    "securities_htm_ac",
        "second_col":   "securities_afs_ac",
        "method":       "sum",
    },
    # * ----------------------------------------------------------------------------------------------------------
    # Create 'securities_fv' from 'securities_htm_fv' and 'securities_afs':
    {
        "new_var":      "securities_fv",  # End of quarter, in thousand of dollars
        "first_col":    "securities_htm_fv",
        "second_col":   "securities_afs_fv",
        "method":       "sum",
    },
    # * ----------------------------------------------------------------------------------------------------------
    #? ----------------------------------------- MATURITY OF TREASURIES ------------------------------------------
    # Create 'treasuries_3m' from rcona549 and rcfda549:
    {
        "new_var":      "treasuries_3m",  # End of quarter, in thousand of dollars
        "first_col":    "rcona549",
        "second_col":   "rcfda549",
        "method":       "first",
    },
    # * ----------------------------------------------------------------------------------------------------------
    # Create 'treasuries_3m_1y' from rcona550 and rcfda550:
    {
        "new_var":      "treasuries_3m_1y",  # End of quarter, in thousand of dollars
        "first_col":    "rcona550",
        "second_col":   "rcfda550",
        "method":       "first",
    },
    # * ----------------------------------------------------------------------------------------------------------
    # Create 'treasuries_1y_3y' from rcona551 and rcfda551:
    {
        "new_var":      "treasuries_1y_3y",  # End of quarter, in thousand of dollars
        "first_col":    "rcona551",
        "second_col":   "rcfda551",
        "method":       "first",
    },
    # * ----------------------------------------------------------------------------------------------------------
    # Create 'treasuries_3y_5y' from rcona552 and rcfda552:
    {
        "new_var":      "treasuries_3y_5y",  # End of quarter, in thousand of dollars
        "first_col":    "rcona552",
        "second_col":   "rcfda552",
        "method":       "first",
    },
    # * ----------------------------------------------------------------------------------------------------------
    # Create 'treasuries_5y_15y' from rcona553 and rcfda553:
    {
        "new_var":      "treasuries_5y_15y",  # End of quarter, in thousand of dollars
        "first_col":    "rcona553",
        "second_col":   "rcfda553",
        "method":       "first",
    },
    # * ----------------------------------------------------------------------------------------------------------
    # Create 'treasuries_15y' from rcona554 and rcfda554:
    {
        "new_var":      "treasuries_15y",  # End of quarter, in thousand of dollars
        "first_col":    "rcona554",
        "second_col":   "rcfda554",
        "method":       "first",
    },
    # * ----------------------------------------------------------------------------------------------------------
    #? --------------------------------------------- MATURITY OF MBS ---------------------------------------------
    # Create 'mbs_3m' from rcona555 and rcfda555:
    {        
        "new_var":      "mbs_3m",  # End of quarter, in thousand of dollars
        "first_col":    "rcona555",
        "second_col":   "rcfda555",
        "method":       "first",
    },
    # * ----------------------------------------------------------------------------------------------------------
    # Create 'mbs_3m_1y' from rcona556 and rcfda556:
    {
        "new_var":      "mbs_3m_1y",  # End of quarter, in thousand of dollars
        "first_col":    "rcona556",
        "second_col":   "rcfda556",
        "method":       "first",
    },
    # * ----------------------------------------------------------------------------------------------------------
    # Create 'mbs_1y_3y' from rcona557 and rcfda557:
    {
        "new_var":      "mbs_1y_3y",  # End of quarter, in thousand of dollars
        "first_col":    "rcona557",
        "second_col":   "rcfda557",
        "method":       "first",
    },
    # * ----------------------------------------------------------------------------------------------------------
    # Create 'mbs_3y_5y' from rcona558 and rcfda558:
    {
        "new_var":      "mbs_3y_5y",  # End of quarter, in thousand of dollars
        "first_col":    "rcona558",
        "second_col":   "rcfda558",
        "method":       "first",
    },
    # * ----------------------------------------------------------------------------------------------------------
    # Create 'mbs_5y_15y' from rcona559 and rcfda559:
    {
        "new_var":      "mbs_5y_15y",  # End of quarter, in thousand of dollars
        "first_col":    "rcona559",
        "second_col":   "rcfda559",
        "method":       "first",
    },
    # * ----------------------------------------------------------------------------------------------------------
    # Create 'mbs_15y' from rcona560 and rcfda560:
    {
        "new_var":      "mbs_15y",  # End of quarter, in thousand of dollars
        "first_col":    "rcona560",
        "second_col":   "rcfda560",
        "method":       "first",
    },
    # * ----------------------------------------------------------------------------------------------------------
    # ? --------------------------------------------- MATURITY SECURITIES ----------------------------------------
    # Create 'securities_3m' from 'mbs_3m' and 'treasuries_3m':
    {
        "new_var":      "securities_3m",  # End of quarter, in thousand of dollars
        "first_col":    "mbs_3m",
        "second_col":   "treasuries_3m",
        "method":       "sum",
    },
    # * ----------------------------------------------------------------------------------------------------------
    # Create 'securities_3m_1y' from 'mbs_3m_1y' and 'treasuries_3m_1y':
    {
        "new_var":      "securities_3m_1y",  # End of quarter, in thousand of dollars
        "first_col":    "mbs_3m_1y",
        "second_col":   "treasuries_3m_1y",
        "method":       "sum",
    },
    # * ----------------------------------------------------------------------------------------------------------
    # Create 'securities_1y_3y' from 'mbs_1y_3y' and 'treasuries_1y_3y':
    {
        "new_var":      "securities_1y_3y",  # End of quarter, in thousand of dollars
        "first_col":    "mbs_1y_3y",
        "second_col":   "treasuries_1y_3y",
        "method":       "sum",
    },
    # * ----------------------------------------------------------------------------------------------------------
    # Create 'securities_3y_5y' from 'mbs_3y_5y' and 'treasuries_3y_5y':
    {
        "new_var":      "securities_3y_5y",  # End of quarter, in thousand of dollars
        "first_col":    "mbs_3y_5y",
        "second_col":   "treasuries_3y_5y",
        "method":       "sum",
    },  
    # * ----------------------------------------------------------------------------------------------------------
    # Create 'securities_5y_15y' from 'mbs_5y_15y' and 'treasuries_5y_15y':
    {
        "new_var":      "securities_5y_15y",  # End of quarter, in thousand of dollars
        "first_col":    "mbs_5y_15y",
        "second_col":   "treasuries_5y_15y",
        "method":       "sum",
    },
    # * ----------------------------------------------------------------------------------------------------------
    # Create 'securities_15y' from 'mbs_15y' and 'treasuries_15y':
    {
        "new_var":      "securities_15y",  # End of quarter, in thousand of dollars
        "first_col":    "mbs_15y",
        "second_col":   "treasuries_15y",
        "method":       "sum",
    },
    # ============================================================================================================
    # ====================================== Schedule RC-C - Detailed Loans ======================================
    # ============================================================================================================
    # ? ------------------------------------------- MATURITY OF LOANS --------------------------------------------
    # --------------------------------------------- RESIDENTIAL LOANS -------------------------------------------
    # Create 'rloans_3m' from rcona564 and rcfda564:
    {
        "new_var":      "rloans_3m",  # End of quarter, in thousand of dollars
        "first_col":    "rcona564",
        "method":       "rename",
    },
    # * ----------------------------------------------------------------------------------------------------------
    # Create 'rloans_3m_1y' from rcona565 and rcfda565:
    {
        "new_var":      "rloans_3m_1y",  # End of quarter, in thousand of dollars
        "first_col":    "rcona565",
        "method":       "rename",
    },
    # * ----------------------------------------------------------------------------------------------------------
    # Create 'rloans_1y_3y' from rcona566 and rcfda566:
    {
        "new_var":      "rloans_1y_3y",  # End of quarter, in thousand of dollars
        "first_col":    "rcona566",
        "method":       "rename",
    },
    # * ----------------------------------------------------------------------------------------------------------
    # Create 'rloans_3y_5y' from rcona567 and rcfda567:
    {
        "new_var":      "rloans_3y_5y",  # End of quarter, in thousand of dollars
        "first_col":    "rcona567",
        "method":       "rename",
    },
    # * ----------------------------------------------------------------------------------------------------------
    # Create 'rloans_5y_15y' from rcona568 and rcfda568:
    {
        "new_var":      "rloans_5y_15y",  # End of quarter, in thousand of dollars
        "first_col":    "rcona568",
        "method":       "rename",
    },
    # * ----------------------------------------------------------------------------------------------------------
    # Create 'rloans_15y' from rcona569 and rcfda569:
    {
        "new_var":      "rloans_15y",  # End of quarter, in thousand of dollars
        "first_col":    "rcona569",
        "method":       "rename",
    },
    # * ----------------------------------------------------------------------------------------------------------
    # --------------------------------------------- ALL LOANS ---------------------------------------------------
    # Create 'all_loans_3m' from rcona570 and rcfda570:
    {
        "new_var":      "all_loans_3m",  # End of quarter, in thousand of dollars
        "first_col":    "rcona570",
        "second_col":   "rcfda570",
        "method":       "first",
    },
    # * ----------------------------------------------------------------------------------------------------------
    # Create 'all_loans_3m_1y' from rcona571 and rcfda571:
    {
        "new_var":      "all_loans_3m_1y",  # End of quarter, in thousand of dollars
        "first_col":    "rcona571",
        "second_col":   "rcfda571",
        "method":       "first",
    },
    # * ----------------------------------------------------------------------------------------------------------
    # Create 'all_loans_1y_3y' from rcona572 and rcfda572:
    {
        "new_var":      "all_loans_1y_3y",  # End of quarter, in thousand of dollars
        "first_col":    "rcona572",
        "second_col":   "rcfda572",
        "method":       "first",
    },
    # * ----------------------------------------------------------------------------------------------------------
    # Create 'all_loans_3y_5y' from rcona573 and rcfda573:
    {
        "new_var":      "all_loans_3y_5y",  # End of quarter, in thousand of dollars
        "first_col":    "rcona573",
        "second_col":   "rcfda573",
        "method":       "first",
    },
    # * ----------------------------------------------------------------------------------------------------------
    # Create 'all_loans_5y_15y' from rcona574 and rcfda574:
    {
        "new_var":      "all_loans_5y_15y",  # End of quarter, in thousand of dollars
        "first_col":    "rcona574",
        "second_col":   "rcfda574",
        "method":       "first",
    },
    # * ----------------------------------------------------------------------------------------------------------
    # Create 'all_loans_15y' from rcona575 and rcfda575:
    {
        "new_var":      "all_loans_15y",  # End of quarter, in thousand of dollars
        "first_col":    "rcona575",
        "second_col":   "rcfda575",
        "method":       "first",
    },
    # * ----------------------------------------------------------------------------------------------------------
    # Create 'loans_3m' from 'rloans_3m' and 'all_loans_3m':
    {
        "new_var":      "loans_3m",  # End of quarter, in thousand of dollars
        "first_col":    "rloans_3m",
        "second_col":   "all_loans_3m",
        "method":       "sum",
    },
    # * ----------------------------------------------------------------------------------------------------------
    # Create 'loans_3m_1y' from 'rloans_3m_1y' and 'all_loans_3m_1y':
    {
        "new_var":      "loans_3m_1y",  # End of quarter, in thousand of dollars
        "first_col":    "rloans_3m_1y",
        "second_col":   "all_loans_3m_1y",
        "method":       "sum",
    },
    # * ----------------------------------------------------------------------------------------------------------
    # Create 'loans_1y_3y' from 'rloans_1y_3y' and 'all_loans_1y_3y':
    {
        "new_var":      "loans_1y_3y",  # End of quarter, in thousand of dollars
        "first_col":    "rloans_1y_3y",
        "second_col":   "all_loans_1y_3y",
        "method":       "sum",
    },
    # * ----------------------------------------------------------------------------------------------------------
    # Create 'loans_3y_5y' from 'rloans_3y_5y' and 'all_loans_3y_5y':
    {
        "new_var":      "loans_3y_5y",  # End of quarter, in thousand of dollars
        "first_col":    "rloans_3y_5y",
        "second_col":   "all_loans_3y_5y",
        "method":       "sum",
    },
    # * ----------------------------------------------------------------------------------------------------------
    # Create 'loans_5y_15y' from 'rloans_5y_15y' and 'all_loans_5y_15y':
    {
        "new_var":      "loans_5y_15y",  # End of quarter, in thousand of dollars
        "first_col":    "rloans_5y_15y",
        "second_col":   "all_loans_5y_15y",
        "method":       "sum",
    },
    # * ----------------------------------------------------------------------------------------------------------
    # Create 'loans_15y' from 'rloans_15y' and 'all_loans_15y':
    {
        "new_var":      "loans_15y",  # End of quarter, in thousand of dollars
        "first_col":    "rloans_15y",
        "second_col":   "all_loans_15y",
        "method":       "sum",
    },
    # * ----------------------------------------------------------------------------------------------------------
    # Starting from 2006-06-30: The FDIC provides information on the number and amount of insured and uninsured deposits.
    #
    # THRESHOLD_Dt = { 100k (before 2009-09-30)
    #               { 250k (after 2009-09-30)
    #
    # THRESHOLD_Rt = {250k (before 2009-09-30)
    #               {250k (after 2009-09-30)
    #
    # TOTAL INSURED DEPOSITS = [AMOUNT OF DEPOSIT ACCOUNTS (EXCLUDING RETIREMENT) <= THRESHOLD_Dt] 
    #                       + [AMOUNT OF DEPOSIT ACCOUNTS (EXCLUDING RETIREMENT) > THRESHOLD_Dt] * THRESHOLD_Dt
    #                       + [AMOUNT OF RETIREMENT ACCOUNTS <= THRESHOLD_Rt] 
    #                       + [AMOUNT OF RETIREMENT ACCOUNTS > THRESHOLD_Rt] * THRESHOLD_Rt
    #
    # TOTAL UNINSURED DEPOSITS = [AMOUNT OF DEPOSIT ACCOUNTS (EXCLUDING RETIREMENT) > THRESHOLD_Dt]
    #                         + [AMOUNT OF RETIREMENT ACCOUNTS > THRESHOLD_Rt] 
    #                         - [AMOUNT OF DEPOSIT ACCOUNTS (EXCLUDING RETIREMENT) > THRESHOLD_Dt] * THRESHOLD_Dt
    #                         - [AMOUNT OF RETIREMENT ACCOUNTS > THRESHOLD_Rt] * THRESHOLD_Rt
    #
    #
    # ============================================================================================================
    # ================== Schedule RC-O - Other Data for Deposit Insurance and FICO Assessments ===================
    # ============================================================================================================
    # * ----------------------------------------------------------------------------------------------------------
    # Create 'amt_nonret_deposit_small' from rconf049:
    {
        "new_var":      "amt_nonret_deposit_small",  # End of quarter, in thousand of dollars
        "first_col":    "rconf049",
        "method":       "rename",
    },
    # Note: The series start in 06/30/2006. The difference between the threshold for retirement and non-retirement
    # is due to the fact that during some time they were insured differently. The limit for non-retirement
    # accounts was $100,000 while for retirement accounts it was $250,000.
    # * ----------------------------------------------------------------------------------------------------------
    # Create 'number_nonret_deposits_small' from rconf050:
    {
        "new_var":      "number_nonret_deposits_small",  # End of
        "first_col":    "rconf050",
        "method":       "rename",
    },
    # * ----------------------------------------------------------------------------------------------------------
    # Create 'amt_nonret_deposits_large' from rconf051:
    {
        "new_var":      "amt_nonret_deposits_large",  # End of quarter, in number of accounts
        "first_col":    "rconf051",
        "method":       "rename",
    },
    # * ----------------------------------------------------------------------------------------------------------
    # Create the "number_nonret_deposits_large" from "rconf052" and "rconf048":
    {
        "new_var":      "number_nonret_deposits_large",  # End of quarter, in number of accounts
        "first_col":    "rconf052",
        "method":       "rename",
    },
    # * ----------------------------------------------------------------------------------------------------------
    # Create 'amt_ret_deposits_small' from rconf045:
    {
        "new_var":      "amt_ret_deposits_small",  # End of quarter
        "first_col":    "rconf045",
        "method":       "rename",
    },
    # * ----------------------------------------------------------------------------------------------------------
    # Create 'number_ret_deposits_small' from rconf046:
    {
        "new_var":      "number_ret_deposits_small",  # End of quarter, in number of accounts
        "first_col":    "rconf046",
        "method":       "rename",
    },
    # * ----------------------------------------------------------------------------------------------------------
    # Create 'amt_ret_deposits_large' from rconf047:
    {
        "new_var":      "amt_ret_deposits_large",  # End of quarter, in number of accounts
        "first_col":    "rconf047",
        "method":       "rename",
    },
    # * ----------------------------------------------------------------------------------------------------------
    # Create 'number_ret_deposits_large' from rconf048:
    {
        "new_var":      "number_ret_deposits_large",  # End of quarter, in number of accounts
        "first_col":    "rconf048",
        "method":       "rename",
    },
    # * ----------------------------------------------------------------------------------------------------------
    # ============================================================================================================
    # ====================================== Schedule RI - Income Statement ======================================
    # ============================================================================================================
    # ? ----------------------------------------- INTEREST INCOME ----------------------------------------------
    # * ----------------------------------------------------------------------------------------------------------
    # Create 'interest_income_loans' from riad4010 using ytd_diff method:
    {
        "new_var":      "interest_income_loans",  # End of quarter, in thousand of dollars
        "first_col":    "riad4010",
        "method":       "ytd_diff",
    },
    # Description: Includes the total of interest and fee income and similar charges levied against all assets classified
    # as loans in Condition reports; including fees on overdrafts. This includes interest on acceptances; commercial paper
    # purchased in the open market; drafts for which the bank has given deposit credit to customers; etc.; and on loan paper
    # which has been rediscounted with other banks; paper sold under repurchase agreements or pledged as collateral to secure
    # bills payable or for any other purpose. Includes loan commitment fees and all yield-related fees on loans held in the
    # bank's portfolio. Excludes fees that are not yield-related; such as mortgage servicing fees and syndication fees 
    # applicable to loans which are not assets of the bank. These fees are reported in 'Other Service Charges; Commissions;
    # and Fees.' 
    # * ----------------------------------------------------------------------------------------------------------
    # Create 'credit_card_interest_income' from riadb485 using ytd_diff method:
    {
        "new_var":      "credit_card_interest_income",  # End of quarter, in thousand of dollars
        "first_col":    "riadb485",
        "method":       "ytd_diff",
    },
    # Description: Includes all interest; fees; and similar charges levied against or associated with all extensions
    # of credit to individuals for household; family; and other personal expenditures arising from credit cards 
    # (in domestic offices) reportable in Schedule RC-C; part I; item 6.a; B538 'Credit cards.'
    # * ----------------------------------------------------------------------------------------------------------
    # Create 'interest_income_leases' from riad4065 using ytd_diff method:
    {
        "new_var":      "interest_income_leases",  # End of quarter, in thousand of dollars
        "first_col":    "riad4065",
        "method":       "ytd_diff",
    },
    # Description: Includes amortized income from direct and leveraged financing leases which relate to
    # 'Lease Financing Receivables (Net of Unearned Income) 
    # * ----------------------------------------------------------------------------------------------------------
    # Create 'interest_income_loans_leases' from 'interest_income_loans' and 'interest_income_leases':
    {
        "new_var":      "interest_income_loans_leases",  # End of quarter, in thousand of dollars
        "first_col":    "interest_income_loans",
        "second_col":   "interest_income_leases",
        "method":       "sum",
    },
    # * ----------------------------------------------------------------------------------------------------------
    # Create "interest_income_treasuries" from riadb488:
    {
        "new_var":      "interest_income_treasuries",  # End of quarter, in thousand of dollars
        "first_col":    "riadb488",
        "method":       "ytd_diff",
    },
    # Description: Includes income from all securities reportable in Schedule RC-B; item 1; 'U.S.Treasury securities;'
    # and item 2; 'U.S. Government agency obligations.' Also; includes accretion of discount on U.S. Treasury bills.
    # * ----------------------------------------------------------------------------------------------------------
    # Create 'interest_income_mbs' from riadb489:
    {
        "new_var":      "interest_income_mbs",  # End of quarter, in thousand of dollars
        "first_col":    "riadb489",
        "method":       "ytd_diff",
    },
    # * ----------------------------------------------------------------------------------------------------------
    # Create "interest_income_other_securities" from riad4060:
    {
        "new_var":      "interest_income_other_securities",  # End of quarter, in thousand of dollars
        "first_col":    "riad4060",
        "method":       "ytd_diff",
    },
    # Description: Includes income from all securities reportable in Schedule RC-B; item 4; 'Mortgage-backed securities.'
    # * ----------------------------------------------------------------------------------------------------------
    # Create 'interest_income_securities' from 'interest_income_treasuries', 'interest_income_mbs' and
    # 'interest_income_other_securities':
    {
        "new_var":      "interest_income_securities",  # End of quarter, in thousand of dollars
        "first_col":    ("interest_income_treasuries", "interest_income_mbs", "interest_income_other_securities"),
        "method":       "sum",
    },
    # Description: Includes income from all securities reportable in Schedule RC-B; item 3; 'Securities issued by states
    # and political subdivisions in the U.S.;' item 5; 'Asset-backed securities;'  item 6; 'Other debt securities;' and item 7;
    # 'Investments in mutual funds and other equity securities with readily determinable fair values.'
    # * ----------------------------------------------------------------------------------------------------------
    # Create 'interest_income_trading_assets' from riad4069:
    {
        "new_var":      "interest_income_trading_assets",  # End of quarter, in thousand of dollars
        "first_col":    "riad4069",
        "method":       "ytd_diff",
    },
    # Description: Includes the interest income earned on assets that are included in 'Trading Assets (3545)'.
    #  Also includes  accretion of discount on assets held in trading accounts that have been issued on a discount basis; such as U.S. Treasury bills and commercial paper.
    # * ----------------------------------------------------------------------------------------------------------
    # Create 'interest_income_ffr_repos' from riad4020:
    {
        "new_var":      "interest_income_ffr_repos",  # End of quarter, in thousand of dollars
        "first_col":    "riad4020",
        "method":       "ytd_diff",
    },
    # Description: 
    # * ----------------------------------------------------------------------------------------------------------
    # Create "other_interest_income" from riad4518:
    {
        "new_var":      "other_interest_income",  # End of quarter, in thousand of dollars
        "first_col":    "riad4518",
        "method":       "ytd_diff",
    },
    # Description:
    # * ----------------------------------------------------------------------------------------------------------
    # Create "total_interest_income" from riad4107:
    {
        "new_var":      "total_interest_income",  # End of quarter, in thousand of dollars
        "first_col":    "riad4107",
        "method":       "ytd_diff",
    },
    # Description:
    # * ----------------------------------------------------------------------------------------------------------
    # ? ----------------------------------------- INTEREST EXPENSE ----------------------------------------------
    # * ----------------------------------------------------------------------------------------------------------
    # Create the "interest_expense_debentures" from riad4200:
    {
        "new_var":      "interest_expense_debentures",  # End of quarter, in thousand of dollars
        "first_col":    "riad4200",
        "method":       "ytd_diff",
    },
    # Description:
    # * ----------------------------------------------------------------------------------------------------------
    # Create 'interest_expense_other' from riad4185
    {
        "new_var":      "interest_expense_other",  # End of quarter, in thousand of dollars
        "first_col":    "riad4185",
        "method":       "ytd_diff",
    },
    # Description:
    # * ----------------------------------------------------------------------------------------------------------
    # Create 'intererest_expense_ffr_repos' from riad4180:
    {
        "new_var":      "interest_expense_ffr_repos",  # End of quarter, in thousand of dollars
        "first_col":    "riad4180",
        "method":       "ytd_diff",
    },
    # Description:
    # * ----------------------------------------------------------------------------------------------------------
    # Create 'interest_expense_trans_deposits' from riad4508:
    {
        "new_var":      "interest_expense_trans_deposits",  # End of quarter, in thousand of dollars
        "first_col":    "riad4508",
        "method":       "ytd_diff",
    },
    # Description:
    # * ----------------------------------------------------------------------------------------------------------
    # Create 'interest_expense_savings_deposits' from riad0093:
    {
        "new_var":      "interest_expense_savings_deposits",  # End of quarter, in thousand of dollars
        "first_col":    "riad0093",
        "method":       "ytd_diff",
    },
    # Description:
    # * ----------------------------------------------------------------------------------------------------------
    # Create 'interest_expense_small_td' from riada518 before 2017-03-31 and from riadhk03 after 2017-03-31:
    {
        "new_var":       "interest_expense_small_td",
        "first_col":     "riada518",         # use this YTD source before switch_date
        "method":        "ytd_diff",         # compute quarter flow = YTD_t - YTD_t-1 (and take YTD if Q1)
        "switch_date":   "2017-03-31",       # inclusive: on/after this date use first_col_post
        "first_col_post":"riadhk03",         # use this YTD source on/after switch_date
    },
    # Description:
    # * ----------------------------------------------------------------------------------------------------------
    # Create 'interest_expense_large_td' from riada517 before 2017-03-31 and from riadhk04 after 2017-03-31:
    {
        "new_var":       "interest_expense_large_td",
        "first_col":     "riada517",         # use this YTD source before switch_date
        "method":        "ytd_diff",         # compute quarter flow = YTD_t - YTD_t-1 (and take YTD if Q1)
        "switch_date":   "2017-03-31",       # inclusive: on/after this date use first_col_post
        "first_col_post":"riadhk04",         # use this YTD source on/after switch_date
    },
    # Description:
    # * ----------------------------------------------------------------------------------------------------------
    # Create 'interest_expense_time_deposits' from 'interest_expense_small_td' and 'interest_expense_large_td':
    {
        "new_var":      "interest_expense_time_deposits",  # End of quarter, in thousand of dollars
        "first_col":    ("interest_expense_small_td", "interest_expense_large_td"),
        "method":       "sum",
    },
    # Description:
    # * ----------------------------------------------------------------------------------------------------------
    # Create 'total_interest_expense' from riad4073:
    {
        "new_var":      "total_interest_expense",  # End of quarter, in thousand of dollars
        "first_col":    "riad4073",
        "method":       "ytd_diff",
    },
    # Description:
    # * ----------------------------------------------------------------------------------------------------------
    # ? ----------------------------------------- NON-INTEREST INCOME --------------------------------------------
    # * ----------------------------------------------------------------------------------------------------------
    # Create 'service_charge_income' from riad4080:
    {
        "new_var":      "service_charge_income",  # End of quarter, in thousand of dollars
        "first_col":    "riad4080",
        "method":       "ytd_diff",
    },
    # Description: Includes amounts charged depositors: (1) for the maintenance of their deposit accounts with the bank;
    # so-called  'maintenance charges'; (2) for their failure to maintain specified minimum deposit balances; (3) based on
    # the number of  checks drawn on and deposits made in their deposit accounts; (4) for checks drawn on so-called 'no minimum balance'
    # deposit accounts; (5) for withdrawals from nontransaction deposit accounts; (6) for the closing of savings accounts 
    # before a specified minimum period of time has elapsed; (7) for accounts which have remained in active for extended 
    # periods of time or which have become dormant; (8) for deposits to or withdrawals from deposit accounts through the use
    # of automated teller machines or remote service units; (9) for the processing of checks drawn against insufficient funds;
    # so-called 'NSF check charges;' that the bank assesses regardless of whether it decides to pay; return; or hold the check.  
    # Excludes subsequent charges levied against overdrawn accounts based on the length of time the account has been  overdrawn;
    # the magnitude of the overdrawn balance; or which are otherwise equivalent to interest; (10) for issuing stop  payment orders;
    # (11) for certifying checks; and (12) for the accumulation or disbursement of funds deposited to  Individual Retirement Accounts
    # (IRAs) or KEOGH plan accounts when not handled by the bank's trust department.  Reported are such commissions and fees received
    # for accounts handled by the bank's trust department in 'Income from Fiduciary Activities (4070)'.
    # * ----------------------------------------------------------------------------------------------------------
    # Create 'other_noninterest_income' from riadb497:
    {
        "new_var":      "other_noninterest_income",  # End of quarter, in thousand of dollars
        "first_col":    "riadb497",
        "method":       "ytd_diff",
    },
    # * ----------------------------------------------------------------------------------------------------------
    # Create 'total_noninterest_income' summing the two previous variables:
    {
        "new_var":      "total_noninterest_income",  # End of quarter, in thousand of dollars
        "first_col":    ("service_charge_income", "other_noninterest_income"),
        "method":       "sum",
    },
    # * ----------------------------------------------------------------------------------------------------------
    # ? ----------------------------------------- OTHER STUFF ------------------------------------------
    # * ----------------------------------------------------------------------------------------------------------
    # Create 'realized_gains_losses_htm_securities' from riad3521:
    {
        "new_var":      "realized_gains_losses_htm_securities",  # End of quarter, in thousand of dollars
        "first_col":    "riad3521",
        "method":       "ytd_diff",
    },
    # Description:  Includes the net gain or loss realized during the calendar year-to-date from the sale; exchange;
    # redemption; or  retirement of all securities that are reportable in Schedules RC (for the FFIEC 031-034 reports;
    # or HC for the FR Y-9C  report); item 1754 'Held-to-maturity securities.' The realized gain or loss on a security
    # is the difference between the  sales price (excluding interest at the coupon rate accrued since the last interest
    # payment date; if any) and its amortized  cost. Also included in this item are write-downs of the cost basis of
    # individual held-to-maturity securities for other than temporary impairments. If the amount reported is a net loss;
    # it is then enclosed in parentheses. Excludes realized gains (losses) on available-for-sale securities
    # (reported in Schedule RI; item 3196 (item 6.b)  for the FFIEC 031-034 reports and in Schedule HI; item 3196 for the
    # FR Y-9C report) and on trading securities  (reported in Schedule RI; item 5408 (item 5.b.(2)) for the FFIEC 034 report;
    # item A220 (item 5.c) for the FFIEC 031;  032; and 033 reports and in Schedule HI; for the FR Y-9C report).
    # Also excludes net gains (losses) from the sale of  detached securities coupons and the sale of ex-coupon securities
    # (reported in 'Other noninterest income (4079)'; or 'Other noninterest expense (4092)'; as appropriate for the FR Y-9C report).
    # * ----------------------------------------------------------------------------------------------------------
    # Create 'realized_gains_losses_afs_securities' from riad3196:
    {
        "new_var":      "realized_gains_losses_afs_securities",  #
        "first_col":    "riad3196",
        "method":       "ytd_diff",
    },
    # Description: Includes the net gain or loss realized during the calendar year to date from the sale; exchange; redemption;
    #  or  retirement of all securities that are reportable in Schedule RC for the FFIEC 031-034 reports and in Schedule HC for
    #  the  FR Y-9C report; item 1773 'Available-for-sale securities.' The realized gain or loss on a security is the difference
    #   between the sales price (excluding interest at the coupon rate accrued since the last interest payment date; if any) and
    #  its  amortized cost. Also included in this item are write-downs of the cost basis of individual available-for-sale
    #  securities for  other than temporary impairments. If the amount reported is a net loss; it is then enclosed in parentheses.
    #  Note: For the FR  Y-9C report; should not adjust for applicable taxes (income taxes applicable to gains (losses) on
    #  available-for-sale securities are included in the applicable income taxes reported in item 4302 and separately reported in
    #  item 4219. Excludes (1) the change in net unrealized holding gains (losses) on available-for-sale securities during the
    #  calendar year to date (reported in Schedule RI-A; for the FFIEC 031-034 reports and in Schedule HI-A;
    # * ---------------------------------------------------------------------------------------------------------- 
    # Create 'realized_gains_losses_securities' from 'realized_gains_losses_htm_securities' and
    # 'realized_gains_losses_afs_securities':
    {
        "new_var":      "realized_gains_losses_securities",  # End of quarter, in thousand of dollars
        "first_col":    ("realized_gains_losses_htm_securities", "realized_gains_losses_afs_securities"),
        "method":       "sum",
    },
    # Description:
    # ? ----------------------------------------- NON-INTEREST EXPENSES ------------------------------------------
    # * ----------------------------------------------------------------------------------------------------------
    # Create 'salaries_expenses' from riad4135:
    {
        "new_var":      "salaries_expenses",  # End of quarter, in thousand of dollars
        "first_col":    "riad4135",
        "method":       "ytd_diff",
    },
    # Description:Includes salaries and benefits of all officers and employees of the bank and its consolidated
    # subsidiaries including guards and contracted guards; temporary office help; dining room and cafeteria employees;
    # and building department officers and employees (including maintenance personnel). Includes as salaries and employee benefits
    # * ----------------------------------------------------------------------------------------------------------
    # Create 'premises_fixed_assets_expenses' from riad4217:
    {
        "new_var":      "premises_fixed_assets_expenses",  # End of quarter, in thousand of dollars
        "first_col":    "riad4217",
        "method":       "ytd_diff",
    },
    # Description:  Includes all noninterest expenses related to the use of premises; equipment; furniture; and fixtures.
    # Deducted is  rental income from gross premises and fixed asset expense. Rental income includes all rentals charged
    # for the use of  buildings not incident to their use by the reporting bank and its consolidated subsidiaries; including
    # rentals by regular  tenants of the bank's buildings; income received from short-term rentals of other bank facilities;
    # and income from  subleases. Also deducted is income from assets that indirectly represent premises; equipment; furniture;
    # or fixtures included in 'Premises and Fixed Assets (2145)'
    # * ----------------------------------------------------------------------------------------------------------
    # Create 'other_noninterest_expenses' from riad4225:
    {
        "new_var":      "other_noninterest_expenses",  # End of quarter, in thousand of dollars
        "first_col":    "riad4092",
        "method":       "ytd_diff",
    },
    # Description:
    # * ----------------------------------------------------------------------------------------------------------
    # Create 'total_noninterest_expenses' summing the three previous variables:
    {
        "new_var":      "total_noninterest_expenses",  # End of quarter, in thousand of dollars
        "first_col":    ("salaries_expenses", "premises_fixed_assets_expenses", "other_noninterest_expenses"),
        "method":       "sum",
    },
    # * ----------------------------------------------------------------------------------------------------------
    # ? --------------------------------------- ADJUSTING FOR DEFAULT --------------------------------------------
    # * ----------------------------------------------------------------------------------------------------------
    # Create 'charge_off_loans' from riad4635:
    {
        "new_var":      "charge_off_loans",  # End of quarter, in thousand of dollars
        "first_col":    "riad4635",
        "method":       "ytd_diff",
    },
    # Description: The amount of gross charge-offs on loans and leases during the calendar year-to-date
    # * ----------------------------------------------------------------------------------------------------------
    # Create 'recoveries_loans' from riad4605:
    {
        "new_var":      "recoveries_loans",  # End of quarter, in thousand of dollars
        "first_col":    "riad4605",
        "method":       "ytd_diff",
    }, 
    # Description: Includes recoveries of amounts previously charged-off against allowance for loan and lease losses
    # during the calendar year-to-date.
    # * ----------------------------------------------------------------------------------------------------------
    # ============================================================================================================
    # ==================================== Schedule RC-E: Deposit Liabilities ====================================
    # ============================================================================================================
    # * ----------------------------------------------------------------------------------------------------------
    # * ----------------------------------------------------------------------------------------------------------
    # * ----------------------------------------------------------------------------------------------------------
    # * ----------------------------------------------------------------------------------------------------------
    # * ----------------------------------------------------------------------------------------------------------
    # * ----------------------------------------------------------------------------------------------------------
    # * ----------------------------------------------------------------------------------------------------------
]