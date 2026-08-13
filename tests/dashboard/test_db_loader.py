import sys
import os
sys.path.append(os.getcwd())

from src.dashboard.utils.db import get_companies, get_ratios, get_sectors, get_pl, get_valuation

def test_get_companies():
    df = get_companies()
    assert len(df) >= 92
    assert "ticker" in df.columns

def test_get_sectors():
    sectors = get_sectors()
    assert len(sectors) == 11
    assert sectors[1] == "IT Services"

def test_get_pl():
    df = get_pl("COMP_01")
    assert len(df) == 10
    assert "sales" in df.columns

def test_get_valuation():
    val = get_valuation("COMP_01")
    assert "pe_ratio" in val
    assert "flag" in val
