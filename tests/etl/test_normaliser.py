import pytest
from src.etl.normaliser import normalize_ticker, normalize_year

def test_normalize_ticker():
    assert normalize_ticker(" reliance ") == "RELIANCE"
    assert normalize_ticker("tcs.ns") == "TCS"
    assert normalize_ticker("infy.bo") == "INFY"
    assert normalize_ticker("hdfcbank-eq") == "HDFCBANK"
    assert normalize_ticker("TATAMOTORS") == "TATAMOTORS"
    assert normalize_ticker(" wipro_NS ") == "WIPRO"
    assert normalize_ticker("icicibank.NS") == "ICICIBANK"
    assert normalize_ticker("sbin.BO") == "SBIN"
    assert normalize_ticker("bhartiartl-EQ") == "BHARTIARTL"
    assert normalize_ticker("itc.NS") == "ITC"
    assert normalize_ticker("  lt  ") == "LT"
    assert normalize_ticker("axisbank.BO") == "AXISBANK"
    assert normalize_ticker("maruti-eq") == "MARUTI"
    assert normalize_ticker("sunpharma.NS") == "SUNPHARMA"
    assert normalize_ticker(None) == ""

def test_normalize_year():
    assert normalize_year("FY2023") == 2023
    assert normalize_year("2022-23") == 2022
    assert normalize_year("2021.0") == 2021
    assert normalize_year(2020) == 2020
    assert normalize_year("Mar-19") == 2019
    assert normalize_year("FY 2018") == 2018
    assert normalize_year("2017/18") == 2017
    assert normalize_year("CY2016") == 2016
    assert normalize_year("2015_FY") == 2015
    assert normalize_year("14") == None
    assert normalize_year(None) == None
    assert normalize_year("2024") == 2024
    assert normalize_year("2025.00") == 2025
    assert normalize_year("FY26") == None
    assert normalize_year("2013-14") == 2013
    assert normalize_year("2012/2013") == 2012
    assert normalize_year("FY2011") == 2011
    assert normalize_year("2010.0") == 2010
    assert normalize_year("2009-10") == 2009
    assert normalize_year("2008") == 2008
