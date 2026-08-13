import sys
import os
sys.path.append(os.getcwd())

from src.analytics.ratios import (
    compute_debt_to_equity,
    compute_interest_coverage_ratio,
    compute_net_debt,
    compute_asset_turnover
)

# Test 1: D/E Debt-Free returns 0.0 (not None)
def test_de_debt_free():
    de_ratio, flag = compute_debt_to_equity(0, 100, 400)
    assert de_ratio == 0.0
    assert flag is False

# Test 2: D/E High Leverage Flag Triggered (>5)
def test_de_high_leverage_flag():
    de_ratio, flag = compute_debt_to_equity(600, 50, 50, broad_sector="Industrial")
    assert de_ratio == 6.0
    assert flag is True

# Test 3: D/E High Leverage Flag Suppressed for Financials
def test_de_financials_carveout():
    de_ratio, flag = compute_debt_to_equity(600, 50, 50, broad_sector="Financials")
    assert de_ratio == 6.0
    assert flag is False

# Test 4: ICR interest=0 returns None & icr_label="Debt Free"
def test_icr_debt_free():
    icr, label, warning = compute_interest_coverage_ratio(200, 50, 0)
    assert icr is None
    assert label == "Debt Free"
    assert warning is False

# Test 5: ICR Warning Flag (< 1.5)
def test_icr_warning_flag():
    icr, label, warning = compute_interest_coverage_ratio(100, 20, 100)
    assert icr == 1.2
    assert warning is True

# Test 6: ICR Normal Case
def test_icr_normal():
    icr, label, warning = compute_interest_coverage_ratio(500, 50, 100)
    assert icr == 5.5
    assert warning is False

# Test 7: Net Debt Computation
def test_net_debt():
    assert compute_net_debt(500, 200) == 300.0

# Test 8: Asset Turnover Normal & Zero Assets Case
def test_asset_turnover():
    assert compute_asset_turnover(1000, 500) == 2.0
    assert compute_asset_turnover(1000, 0) is None
