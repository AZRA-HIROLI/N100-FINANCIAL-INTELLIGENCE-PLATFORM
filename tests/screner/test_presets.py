import sys
import os
import sqlite3
import pandas as pd

sys.path.append(os.getcwd())
from src.screener.engine import apply_screener_filters, load_screener_config

def test_all_presets_return_valid_company_counts():
    conn = sqlite3.connect("db/nifty100_v3.db")
    df_2023 = pd.read_sql_query("""
        SELECT c.company_id, c.sector_id, p.sales, p.net_profit,
               fr.return_on_equity_pct, fr.debt_to_equity, fr.free_cash_flow_cr,
               fr.revenue_cagr_5yr, fr.pat_cagr_5yr, fr.dividend_payout_ratio_pct,
               fr.composite_quality_score
        FROM companies c
        JOIN financial_ratios fr ON c.company_id = fr.company_id
        JOIN profitandloss p ON c.company_id = p.company_id AND fr.year = p.year
        WHERE fr.year = 2023
    """, conn)
    conn.close()

    cfg = load_screener_config("config/screener_config.json")
    for name, filters in cfg["presets"].items():
        res = apply_screener_filters(df_2023, filters)
        assert 5 <= len(res) <= 50, f"Preset {name} returned {len(res)} companies (expected 5-50)"
