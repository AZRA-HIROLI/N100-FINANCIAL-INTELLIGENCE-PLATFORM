import pandas as pd
import numpy as np

def compute_valuation_metrics(df: pd.DataFrame) -> pd.DataFrame:
    res_df = df.copy()

    # 1. Calculate FCF Yield %
    if "free_cash_flow_cr" in res_df.columns and "market_cap_cr" in res_df.columns:
        res_df["fcf_yield_pct"] = round((res_df["free_cash_flow_cr"] / res_df["market_cap_cr"].replace(0, np.nan)) * 100.0, 2)
    else:
        res_df["fcf_yield_pct"] = 3.5

    # 2. Sector Median P/E Calculation
    if "sector_name" in res_df.columns and "pe_ratio" in res_df.columns:
        sector_medians = res_df.groupby("sector_name")["pe_ratio"].transform("median")
        res_df["sector_median_pe"] = round(sector_medians, 2)
        res_df["pe_vs_sector_median_pct"] = round(((res_df["pe_ratio"] - res_df["sector_median_pe"]) / res_df["sector_median_pe"].replace(0, np.nan)) * 100.0, 2)
    else:
        res_df["sector_median_pe"] = 25.0
        res_df["pe_vs_sector_median_pct"] = 0.0

    # 3. Apply Overvaluation / Discount Flag Logic
    def assign_flag(row):
        pe = row.get("pe_ratio", 25.0)
        s_med = row.get("sector_median_pe", 25.0)
        if pd.isna(pe) or pd.isna(s_med) or s_med <= 0:
            return "Fair"
        if pe > (s_med * 1.5):
            return "Caution"
        elif pe < (s_med * 0.7):
            return "Discount"
        return "Fair"

    res_df["flag"] = res_df.apply(assign_flag, axis=1)
    return res_df
