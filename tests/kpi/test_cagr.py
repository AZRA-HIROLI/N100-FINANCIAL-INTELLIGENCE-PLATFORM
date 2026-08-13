import sys
import os
sys.path.append(os.getcwd())

from src.analytics.cagr import compute_cagr, compute_series_cagr

# Test 1: Normal CAGR (100 -> 200 in 3 years)
def test_cagr_normal():
    val, flag = compute_cagr(100.0, 200.0, 3)
    assert val == 25.99
    assert flag == "NORMAL"

# Test 2: Decline to Loss (100 -> -50 in 5 years)
def test_cagr_decline_to_loss():
    val, flag = compute_cagr(100.0, -50.0, 5)
    assert val is None
    assert flag == "DECLINE_TO_LOSS"

# Test 3: Turnaround (-50 -> 100 in 5 years)
def test_cagr_turnaround():
    val, flag = compute_cagr(-50.0, 100.0, 5)
    assert val is None
    assert flag == "TURNAROUND"

# Test 4: Both Negative (-100 -> -50 in 3 years)
def test_cagr_both_negative():
    val, flag = compute_cagr(-100.0, -50.0, 3)
    assert val is None
    assert flag == "BOTH_NEGATIVE"

# Test 5: Zero Base (0 -> 100 in 5 years)
def test_cagr_zero_base():
    val, flag = compute_cagr(0.0, 100.0, 5)
    assert val is None
    assert flag == "ZERO_BASE"

# Test 6: Insufficient Years / Data
def test_cagr_insufficient():
    val, flag = compute_cagr(None, 100.0, 5)
    assert val is None
    assert flag == "INSUFFICIENT"

# Test 7: Series CAGR Normal 5-Year
def test_series_cagr_normal():
    data = [{'year': 2018, 'sales': 100.0}, {'year': 2023, 'sales': 200.0}]
    val, flag = compute_series_cagr(data, 'sales', 5)
    assert val == 14.87
    assert flag == "NORMAL"

# Test 8: Series CAGR Insufficient Data Points
def test_series_cagr_insufficient():
    data = [{'year': 2021, 'sales': 100.0}, {'year': 2023, 'sales': 200.0}]
    val, flag = compute_series_cagr(data, 'sales', 5)
    assert val is None
    assert flag == "INSUFFICIENT"

# Test 9: 10-Year CAGR Edge Case
def test_cagr_10yr():
    val, flag = compute_cagr(100.0, 259.37, 10)
    assert val == 10.0
    assert flag == "NORMAL"

# Test 10: Decline to Zero
def test_cagr_decline_to_zero():
    val, flag = compute_cagr(100.0, 0.0, 5)
    assert val is None
    assert flag == "DECLINE_TO_LOSS"
