from fastapi import APIRouter, HTTPException

router = APIRouter(tags=["Peers & Comparison"])

@router.get("/peers/{group_name}", summary="Get peer group percentile ranks")
async def get_peer_group(group_name: str):
    if group_name.lower() not in ["it_large_cap", "banking_majors", "pharma_bluechip"]:
        raise HTTPException(status_code=404, detail=f"Peer group '{group_name}' not found.")
    return {"peer_group": group_name, "constituents": ["TCS", "INFY", "WIPRO"], "percentile_rankings": {"TCS": {"roe_rank": 95}}}

@router.get("/companies/{ticker}/peers/compare", summary="Get radar comparison data")
async def compare_company_peers(ticker: str):
    return {
        "ticker": ticker.upper(),
        "axes": ["ROE", "ROCE", "OPM", "NPM", "Asset Turnover", "Interest Coverage", "FCF Conversion", "Sales CAGR"],
        "company_values": [43.5, 51.2, 24.0, 16.5, 1.3, 18.2, 90.0, 12.5],
        "peer_group_average": [20.1, 22.0, 18.5, 12.0, 1.1, 10.4, 75.0, 10.0]
    }
