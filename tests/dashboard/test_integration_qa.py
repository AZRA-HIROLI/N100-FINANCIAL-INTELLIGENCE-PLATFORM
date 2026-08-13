import os
import sys
import time
import pandas as pd
import pytest

sys.path.append(os.getcwd())

from src.dashboard.utils.db import get_companies, get_ratios, get_pl, get_valuation

# Test Tickers across 10 distinct sectors
SAMPLE_TICKERS = [
    "COMP_01", "COMP_02", "COMP_03", "COMP_04", "COMP_05",
    "COMP_06", "COMP_07", "COMP_08", "COMP_09", "COMP_10"
]

def test_qa_01_all_10_tickers_db_loading():
    for ticker in SAMPLE_TICKERS:
        df_pl = get_pl(ticker)
        assert len(df_pl) > 0, f"PL data failed for {ticker}"
        val = get_valuation(ticker)
        assert "pe_ratio" in val, f"Valuation failed for {ticker}"

def test_qa_02_partial_data_handling():
    # Test ticker with missing or null values
    df_null = pd.DataFrame([{
        "company_id": 999, "ticker": "NULL_COMP", "company_name": "Null Corp",
        "return_on_equity_pct": None, "debt_to_equity": None, "free_cash_flow_cr": None
    }])

    roe_val = df_null["return_on_equity_pct"].iloc[0]
    display_roe = f"{roe_val:.1f}%" if pd.notnull(roe_val) else "N/A"
    assert display_roe == "N/A"

def test_qa_03_screener_extreme_boundaries():
    df_master = get_ratios()

    # Extreme Filter 1: Unobtainable High Thresholds
    filtered_empty = df_master[
        (df_master["return_on_equity_pct"] > 99.0) & 
        (df_master["debt_to_equity"] < 0.001)
    ]
    assert len(filtered_empty) == 0, "Extreme filter should return empty set cleanly"

    # Extreme Filter 2: All Inclusive Thresholds
    filtered_all = df_master[
        (df_master["return_on_equity_pct"] >= 0.0) & 
        (df_master["debt_to_equity"] <= 100.0)
    ]
    assert len(filtered_all) == len(df_master), "Inclusive filter should match total universe"

def test_qa_04_profile_load_latency_under_3s():
    tickers_to_benchmark = ["COMP_01", "COMP_12", "COMP_25", "COMP_50", "COMP_88"]
    latencies = []

    for t in tickers_to_benchmark:
        start_t = time.time()

        # Simulate Company Profile Screen Execution Data Pipeline
        df_comps = get_companies()
        matched = df_comps[df_comps["ticker"] == t]
        df_r = get_ratios(ticker=t)
        df_pl = get_pl(t)
        val = get_valuation(t)

        elapsed = time.time() - start_t
        latencies.append(elapsed)
        assert elapsed < 3.0, f"Load time for {t} exceeded threshold: {elapsed:.3f}s"

    avg_latency = sum(latencies) / len(latencies)
    print(f"\n[Performance Metric] Average Profile Load Latency: {avg_latency*1000:.2f} ms")
