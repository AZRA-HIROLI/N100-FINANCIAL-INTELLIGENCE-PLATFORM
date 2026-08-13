import pandas as pd
import numpy as np

def compute_peer_percentiles(df: pd.DataFrame, peer_col: str = "peer_group_name") -> pd.DataFrame:
    metrics_to_rank = [
        "return_on_equity_pct",
        "roce_pct",
        "net_profit_margin_pct",
        "debt_to_equity",
        "free_cash_flow_cr",
        "pat_cagr_5yr",
        "revenue_cagr_5yr",
        "eps_cagr_5yr",
        "interest_coverage",
        "asset_turnover"
    ]

    ranked_records = []

    for peer_group, group in df.groupby(peer_col):
        if pd.isna(peer_group) or str(peer_group).strip() == "":
            continue

        group_len = len(group)

        for metric in metrics_to_rank:
            if metric not in group.columns:
                continue

            ascending_order = False if metric == "debt_to_equity" else True

            if group_len > 1:
                ranks = group[metric].rank(pct=True, ascending=ascending_order).fillna(0.50)
            else:
                ranks = pd.Series(1.00, index=group.index)

            for idx, row in group.iterrows():
                ranked_records.append({
                    "company_id": int(row["company_id"]),
                    "peer_group_name": str(peer_group),
                    "metric": metric,
                    "value": row[metric] if pd.notnull(row[metric]) else None,
                    "percentile_rank": round(float(ranks.loc[idx]), 4),
                    "year": int(row["year"])
                })

    return pd.DataFrame(ranked_records)
