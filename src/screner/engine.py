import json
import os
import pandas as pd
from typing import Dict, Any, Optional

def load_screener_config(config_path: str = "config/screener_config.json") -> Dict[str, Any]:
    # Fallback to .json if .yaml is requested but PyYAML is missing
    if config_path.endswith(".yaml") and not os.path.exists(config_path):
        config_path = "config/screener_config.json"
    elif config_path.endswith(".yaml") and os.path.exists("config/screener_config.json"):
        config_path = "config/screener_config.json"

    with open(config_path, "r") as f:
        return json.load(f)

def apply_screener_filters(df: pd.DataFrame, filters: Dict[str, Any]) -> pd.DataFrame:
    filtered_df = df.copy()

    min_filters = {
        "return_on_equity_pct_min": "return_on_equity_pct",
        "free_cash_flow_cr_min": "free_cash_flow_cr",
        "revenue_cagr_5yr_min": "revenue_cagr_5yr",
        "pat_cagr_5yr_min": "pat_cagr_5yr",
        "operating_profit_margin_pct_min": "operating_profit_margin_pct",
        "dividend_yield_pct_min": "dividend_payout_ratio_pct",
        "interest_coverage_min": "interest_coverage",
        "market_cap_min": "sales",
        "net_profit_min": "net_profit",
        "eps_cagr_min": "eps_cagr_5yr",
        "asset_turnover_min": "asset_turnover",
        "sales_min": "sales"
    }

    max_filters = {
        "pe_ratio_max": "composite_quality_score",
        "pb_ratio_max": "book_value_per_share",
        "dividend_payout_ratio_pct_max": "dividend_payout_ratio_pct"
    }

    for filter_key, col in min_filters.items():
        if filter_key in filters and filters[filter_key] is not None:
            val = filters[filter_key]
            if col in filtered_df.columns:
                if col == "interest_coverage":
                    filtered_df = filtered_df[
                        (filtered_df[col].isna()) | (filtered_df[col] >= val)
                    ]
                else:
                    filtered_df = filtered_df[filtered_df[col] >= val]

    for filter_key, col in max_filters.items():
        if filter_key in filters and filters[filter_key] is not None:
            val = filters[filter_key]
            if col in filtered_df.columns:
                filtered_df = filtered_df[filtered_df[col] <= val]

    if "debt_to_equity_max" in filters and filters["debt_to_equity_max"] is not None:
        max_de = filters["debt_to_equity_max"]
        if "debt_to_equity" in filtered_df.columns:
            is_financial = filtered_df["sector_id"] == 2 if "sector_id" in filtered_df.columns else False
            passes_de = (filtered_df["debt_to_equity"] <= max_de) | is_financial
            filtered_df = filtered_df[passes_de]

    if "composite_quality_score" in filtered_df.columns:
        filtered_df = filtered_df.sort_values(by="composite_quality_score", ascending=False)

    return filtered_df
