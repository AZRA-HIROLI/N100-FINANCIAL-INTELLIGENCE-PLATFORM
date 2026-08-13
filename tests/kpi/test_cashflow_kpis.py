import sys
import os
sys.path.append(os.getcwd())

from src.analytics.cashflow_kpis import (
    compute_free_cash_flow,
    compute_cfo_quality_score,
    compute_capex_intensity,
    compute_fcf_conversion_rate,
    classify_capital_allocation_pattern
)

# Test 1: FCF Calculation
def test_fcf():
    assert compute_free_cash_flow(500.0, -200.0) == 300.0
    assert compute_free_cash_flow(100.0, -300.0) == -200.0

# Test 2: CFO Quality Score
def test_cfo_quality():
    score, label = compute_cfo_quality_score(150.0, 100.0)
    assert score == 1.5
    assert label == "High Quality"

# Test 3: CFO Quality Score PAT=0
def test_cfo_quality_zero_pat():
    score, label = compute_cfo_quality_score(150.0, 0.0)
    assert score is None
    assert label == "UNDEFINED"

# Test 4: CapEx Intensity
def test_capex_intensity():
    intensity, label = compute_capex_intensity(-20.0, 1000.0)
    assert intensity == 2.0
    assert label == "Asset Light"

# Test 5: Capital Allocation Patterns
def test_capital_allocation_classifier():
    assert classify_capital_allocation_pattern(500, -200, -100) == "Reinvestor"
    assert classify_capital_allocation_pattern(500, -200, -100, cfo_pat_ratio=1.5) == "Shareholder Returns"
    assert classify_capital_allocation_pattern(-100, 50, 50) == "Distress Signal"
    assert classify_capital_allocation_pattern(-100, -50, 100) == "Growth Funded by Debt"
