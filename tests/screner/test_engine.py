import sys
import os
import pandas as pd
sys.path.append(os.getcwd())

from src.screener.engine import apply_screener_filters, load_screener_config

def test_load_config():
    cfg = load_screener_config("config/screener_config.yaml")
    assert "presets" in cfg
    assert "quality_compounder" in cfg["presets"]

def test_quality_compounder_filter():
    data = [
        {"company_id": 1, "sector_id": 1, "return_on_equity_pct": 20.0, "debt_to_equity": 0.5, "free_cash_flow_cr": 100.0, "revenue_cagr_5yr": 12.0, "composite_quality_score": 85.0},
        {"company_id": 2, "sector_id": 1, "return_on_equity_pct": 10.0, "debt_to_equity": 0.2, "free_cash_flow_cr": 50.0, "revenue_cagr_5yr": 15.0, "composite_quality_score": 60.0},
        {"company_id": 3, "sector_id": 2, "return_on_equity_pct": 18.0, "debt_to_equity": 8.5, "free_cash_flow_cr": 200.0, "revenue_cagr_5yr": 14.0, "composite_quality_score": 90.0}
    ]
    df = pd.DataFrame(data)
    filters = {"return_on_equity_pct_min": 15.0, "debt_to_equity_max": 1.0, "free_cash_flow_cr_min": 0.0, "revenue_cagr_5yr_min": 10.0}

    res = apply_screener_filters(df, filters)
    # Company 1 passes, Company 2 fails ROE, Company 3 passes because sector_id 2 bypasses D/E filter
    assert len(res) == 2
    assert list(res["company_id"]) == [3, 1]
