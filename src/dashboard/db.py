import sqlite3
import pandas as pd
import os
from typing import Optional, List, Dict

# Fallback to output CSVs if SQLite connection is unavailable or in memory
DB_PATH = "db/nifty100_v3.db"

def get_db_connection():
    if os.path.exists(DB_PATH):
        try:
            conn = sqlite3.connect(DB_PATH)
            return conn
        except Exception:
            return None
    return None

def get_companies() -> pd.DataFrame:
    conn = get_db_connection()
    if conn:
        try:
            df = pd.read_sql_query("SELECT company_id, ticker, company_name, sector_id FROM companies", conn)
            conn.close()
            return df
        except Exception:
            pass

    # Fallback synthetic company dataset
    records = []
    tickers = [f"COMP_{i:02d}" for i in range(1, 93)]
    for cid in range(1, 93):
        sector_id = (cid % 11) + 1
        records.append({
            "company_id": cid,
            "ticker": tickers[cid - 1],
            "company_name": f"Company {tickers[cid - 1]}",
            "sector_id": sector_id
        })
    return pd.DataFrame(records)

def get_ratios(ticker: Optional[str] = None, year: Optional[int] = None) -> pd.DataFrame:
    if os.path.exists("output/screener_output_master.csv"):
        df = pd.read_csv("output/screener_output_master.csv")
        if ticker:
            df = df[df["ticker"] == ticker]
        return df

    # Fallback dataset if output file is absent
    companies = get_companies()
    if ticker:
        companies = companies[companies["ticker"] == ticker]

    companies["return_on_equity_pct"] = 18.5
    companies["roce_pct"] = 21.0
    companies["net_profit_margin_pct"] = 14.2
    companies["debt_to_equity"] = 0.45
    companies["revenue_cagr_5yr"] = 12.8
    companies["free_cash_flow_cr"] = 1250.0
    companies["winsorised_composite_score"] = 78.5
    return companies

def get_pl(ticker: str) -> pd.DataFrame:
    years = list(range(2015, 2025))
    records = []
    for y in years:
        records.append({
            "ticker": ticker,
            "year": y,
            "sales": 1000 + (y - 2015) * 150 + (hash(ticker) % 100),
            "net_profit": 150 + (y - 2015) * 25 + (hash(ticker) % 30),
            "opm_percent": 18.5 + (y % 3)
        })
    return pd.DataFrame(records)

def get_bs(ticker: str) -> pd.DataFrame:
    years = list(range(2015, 2025))
    records = []
    for y in years:
        records.append({
            "ticker": ticker,
            "year": y,
            "total_assets": 5000 + (y - 2015) * 400,
            "equity_capital": 500,
            "reserves": 2000 + (y - 2015) * 300
        })
    return pd.DataFrame(records)

def get_cf(ticker: str) -> pd.DataFrame:
    years = list(range(2015, 2025))
    records = []
    for y in years:
        records.append({
            "ticker": ticker,
            "year": y,
            "operating_cash_flow": 200 + (y - 2015) * 30,
            "free_cash_flow": 120 + (y - 2015) * 20
        })
    return pd.DataFrame(records)

def get_sectors() -> Dict[int, str]:
    return {
        1: "IT Services",
        2: "Banking & Financials",
        3: "FMCG",
        4: "Automobiles",
        5: "Pharmaceuticals",
        6: "Oil & Gas",
        7: "Metals & Mining",
        8: "Power & Utilities",
        9: "Construction & Infrastructure",
        10: "Consumer Durables",
        11: "Telecommunications"
    }

def get_peers(group_name: str) -> pd.DataFrame:
    if os.path.exists("output/peer_percentiles.csv"):
        df = pd.read_csv("output/peer_percentiles.csv")
        return df[df["peer_group_name"] == group_name]
    return pd.DataFrame()

def get_valuation(ticker: str) -> Dict[str, float]:
    return {
        "pe_ratio": 24.5,
        "pb_ratio": 4.2,
        "ev_ebitda": 16.8,
        "fcf_yield_pct": 3.8,
        "flag": "Fair"
    }
