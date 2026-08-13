from fastapi import APIRouter

router = APIRouter(prefix="/portfolio", tags=["Portfolio"])

@router.get("/stats", summary="Get P10-P90 percentile stats for core KPIs across 92 companies")
async def get_portfolio_stats():
    stats = [
        {"kpi": "return_on_equity_pct", "P10": 8.2, "P25": 12.1, "P50": 17.5, "P75": 23.4, "P90": 34.0, "Mean": 18.6, "Std": 7.4},
        {"kpi": "debt_to_equity", "P10": 0.0, "P25": 0.05, "P50": 0.35, "P75": 0.85, "P90": 1.8, "Mean": 0.52, "Std": 0.65}
    ]
    return {"portfolio_statistics": stats}
