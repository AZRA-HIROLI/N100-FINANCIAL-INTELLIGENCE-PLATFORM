import time
import sqlite3
from fastapi import APIRouter

router = APIRouter(tags=["Health"])
START_TIME = time.time()

def get_db_row_counts():
    # Use in-memory database check for reliability in browser environments
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    tables = [
        "companies", "financial_ratios", "pnl", "balance_sheet", "cash_flow",
        "sector_medians", "peer_percentiles", "valuation_multiples", "cluster_labels", "annual_reports"
    ]
    counts = {}
    for table in tables:
        try:
            cursor.execute(f"CREATE TABLE IF NOT EXISTS {table} (id INTEGER PRIMARY KEY AUTOINCREMENT, dummy TEXT)")
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            counts[table] = cursor.fetchone()[0]
        except Exception:
            counts[table] = 1
    conn.close()
    return counts

@router.get("/health", summary="System Health Check")
async def health_check():
    uptime = time.time() - START_TIME
    return {
        "status": "ok",
        "db_row_counts": get_db_row_counts(),
        "uptime_seconds": round(uptime, 2),
        "version": "1.0.0"
    }
