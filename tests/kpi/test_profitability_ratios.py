import sys
import os
sys.path.append(os.getcwd())

from src.analytics.ratios import (
    compute_net_profit_margin,
    compute_operating_profit_margin,
    compute_return_on_equity,
    compute_return_on_capital_employed,
    compute_return_on_assets
)

# Test 1: NPM Normal Case
def test_npm_normal():
    assert compute_net_profit_margin(150, 1000) == 15.0

# Test 2: NPM Zero Denominator (Sales = 0)
def test_npm_zero_sales():
    assert compute_net_profit_margin(150, 0) is None

# Test 3: OPM Cross-Check Mismatch Logging (>1% diff)
def test_opm_mismatch(caplog):
    val = compute_operating_profit_margin(200, 1000, opm_percentage_source=25.0)
    assert val == 20.0
    assert "OPM mismatch > 1%" in caplog.text

# Test 4: ROE Normal Case
def test_roe_normal():
    assert compute_return_on_equity(200, 100, 900) == 20.0

# Test 5: ROE Negative / Zero Equity
def test_roe_negative_equity():
    assert compute_return_on_equity(200, 100, -200) is None

# Test 6: ROCE Normal Case
def test_roce_normal():
    assert compute_return_on_capital_employed(300, 100, 900, 500) == 20.0

# Test 7: ROCE Financials Broad Sector Carve-Out
def test_roce_financials_sector():
    val = compute_return_on_capital_employed(300, 100, 900, 500, broad_sector="Financials")
    assert val == 20.0

# Test 8: ROA Zero Assets
def test_roa_zero_assets():
    assert compute_return_on_assets(100, 0) is None
