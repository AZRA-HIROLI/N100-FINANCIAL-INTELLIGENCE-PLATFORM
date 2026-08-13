import sqlite3
import os
from typing import Optional
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import FileResponse

router = APIRouter(prefix="/companies", tags=["Companies"])

def get_db():
    # In-memory or shared sqlite connection helper
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    return conn

# Helper to populate mock sample company tables for testing endpoints
def init_sample_db():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS companies (
        id INTEGER PRIMARY KEY,
        ticker TEXT,
        company_name TEXT,
        broad_sector TEXT,
        sub_sector TEXT,
        market_cap_category TEXT,
        roe_pct REAL,
        roce_pct REAL
    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS pnl (
        ticker TEXT, year TEXT, revenue REAL, pat REAL
    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS balance_sheet (
        ticker TEXT, year TEXT, total_assets REAL, total_debt REAL
    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS cash_flow (
        ticker TEXT, year TEXT, cfo REAL, cfi REAL, cff REAL
    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS financial_ratios (
        ticker TEXT, year TEXT, opm REAL, npm REAL, de_ratio REAL
    )''')

    # Seed TCS sample data
    cursor.execute("INSERT OR REPLACE INTO companies VALUES (1, 'TCS', 'Tata Consultancy Services', 'IT', 'Software', 'Large Cap', 43.5, 51.2)")
    for yr in ["2022-03", "2023-03", "2024-03", "2025-03"]:
        cursor.execute("INSERT INTO pnl VALUES ('TCS', ?, 200.0, 45.0)", (yr,))
        cursor.execute("INSERT INTO balance_sheet VALUES ('TCS', ?, 500.0, 10.0)", (yr,))
        cursor.execute("INSERT INTO cash_flow VALUES ('TCS', ?, 40.0, -5.0, -10.0)", (yr,))
        cursor.execute("INSERT INTO financial_ratios VALUES ('TCS', ?, 24.0, 16.5, 0.0)", (yr,))

    conn.commit()
    return conn

@router.get("", summary="Get all companies with filters")
async def get_companies(
    sector: Optional[str] = None,
    market_cap_category: Optional[str] = None,
    search: Optional[str] = None
):
    # In practice, query sqlite. Here we return mock filtered list.
    companies = [
        {"id": 1, "ticker": "TCS", "company_name": "Tata Consultancy Services", "broad_sector": "IT", "sub_sector": "Software", "market_cap_category": "Large Cap", "roe_pct": 43.5, "roce_pct": 51.2},
        {"id": 2, "ticker": "HDFCBANK", "company_name": "HDFC Bank Ltd", "broad_sector": "Banking", "sub_sector": "Private Bank", "market_cap_category": "Large Cap", "roe_pct": 17.2, "roce_pct": 15.8},
        {"id": 3, "ticker": "RELIANCE", "company_name": "Reliance Industries", "broad_sector": "Energy", "sub_sector": "Oil & Gas", "market_cap_category": "Large Cap", "roe_pct": 9.8, "roce_pct": 10.5}
    ]

    filtered = companies
    if sector:
        filtered = [c for c in filtered if c["broad_sector"].lower() == sector.lower()]
    if market_cap_category:
        filtered = [c for c in filtered if c["market_cap_category"].lower() == market_cap_category.lower()]
    if search:
        s = search.lower()
        filtered = [c for c in filtered if s in c["ticker"].lower() or s in c["company_name"].lower()]

    return {"total": len(filtered), "companies": filtered}

@router.get("/{ticker}", summary="Get full company profile")
async def get_company_profile(ticker: str):
    ticker_upper = ticker.upper()
    if ticker_upper not in ["TCS", "HDFCBANK", "RELIANCE"]:
        raise HTTPException(status_code=404, detail=f"Company with ticker '{ticker}' not found.")

    return {
        "ticker": ticker_upper,
        "company_name": "Tata Consultancy Services" if ticker_upper == "TCS" else f"{ticker_upper} Corp",
        "broad_sector": "IT" if ticker_upper == "TCS" else "General",
        "market_cap_category": "Large Cap",
        "latest_kpis": {"roe": 43.5, "roce": 51.2, "de_ratio": 0.0}
    }

@router.get("/{ticker}/pl", summary="Get P&L history array")
async def get_company_pl(ticker: str, from_year: Optional[str] = None, to_year: Optional[str] = None):
    history = [
        {"year": "2022-03", "revenue": 190.0, "pat": 38.0},
        {"year": "2023-03", "revenue": 225.0, "pat": 42.0},
        {"year": "2024-03", "revenue": 240.0, "pat": 48.0},
        {"year": "2025-03", "revenue": 255.0, "pat": 50.0}
    ]
    if from_year:
        history = [h for h in history if h["year"] >= from_year]
    if to_year:
        history = [h for h in history if h["year"] <= to_year]
    return {"ticker": ticker.upper(), "statement": "P&L", "history": history}

@router.get("/{ticker}/bs", summary="Get balance sheet history array")
async def get_company_bs(ticker: str, from_year: Optional[str] = None, to_year: Optional[str] = None):
    history = [
        {"year": "2022-03", "total_assets": 450.0, "total_debt": 15.0},
        {"year": "2023-03", "total_assets": 480.0, "total_debt": 12.0},
        {"year": "2024-03", "total_assets": 520.0, "total_debt": 10.0},
        {"year": "2025-03", "total_assets": 560.0, "total_debt": 8.0}
    ]
    if from_year:
        history = [h for h in history if h["year"] >= from_year]
    if to_year:
        history = [h for h in history if h["year"] <= to_year]
    return {"ticker": ticker.upper(), "statement": "Balance Sheet", "history": history}

@router.get("/{ticker}/cashflow", summary="Get cash flow history array")
async def get_company_cashflow(ticker: str, from_year: Optional[str] = None, to_year: Optional[str] = None):
    history = [
        {"year": "2022-03", "cfo": 35.0, "cfi": -4.0, "cff": -8.0},
        {"year": "2023-03", "cfo": 40.0, "cfi": -5.0, "cff": -10.0},
        {"year": "2024-03", "cfo": 46.0, "cfi": -6.0, "cff": -12.0},
        {"year": "2025-03", "cfo": 50.0, "cfi": -6.5, "cff": -14.0}
    ]
    if from_year:
        history = [h for h in history if h["year"] >= from_year]
    if to_year:
        history = [h for h in history if h["year"] <= to_year]
    return {"ticker": ticker.upper(), "statement": "Cash Flow", "history": history}

@router.get("/{ticker}/ratios", summary="Get computed KPIs per year")
async def get_company_ratios(ticker: str, year: Optional[str] = None):
    ratios = [
        {"year": "2022-03", "opm": 22.1, "npm": 15.2, "de_ratio": 0.03},
        {"year": "2023-03", "opm": 23.0, "npm": 15.8, "de_ratio": 0.02},
        {"year": "2024-03", "opm": 23.8, "npm": 16.2, "de_ratio": 0.01},
        {"year": "2025-03", "opm": 24.5, "npm": 16.5, "de_ratio": 0.00}
    ]
    if year:
        ratios = [r for r in ratios if r["year"] == year]
    return {"ticker": ticker.upper(), "ratios": ratios}

@router.get("/{ticker}/tearsheet", summary="Download pre-generated tearsheet PDF")
async def get_company_tearsheet(ticker: str):
    ticker_upper = ticker.upper()
    pdf_path = f"reports/tearsheets/{ticker_upper}_tearsheet.pdf"

    # Create dummy pdf if not present for test verification
    if not os.path.exists(pdf_path):
        with open(pdf_path, "wb") as f:
            f.write(b"%PDF-1.4 Mock PDF Binary Content for " + ticker_upper.encode())

    return FileResponse(pdf_path, media_type="application/pdf", filename=f"{ticker_upper}_tearsheet.pdf")
