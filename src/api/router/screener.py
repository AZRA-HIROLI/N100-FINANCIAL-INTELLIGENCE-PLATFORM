from typing import Optional
from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/screener", tags=["Screener"])

@router.get("", summary="Filter companies using financial screener parameters")
async def run_screener(
    min_roe: Optional[float] = None,
    max_de: Optional[float] = None,
    min_fcf: Optional[float] = None,
    sector: Optional[str] = None,
    min_rev_cagr_5yr: Optional[float] = None,
    max_pe: Optional[float] = None
):
    if min_roe is not None and min_roe > 100:
        raise HTTPException(status_code=400, detail="Invalid parameter: min_roe cannot exceed 100%.")
    if max_de is not None and max_de < 0:
        raise HTTPException(status_code=400, detail="Invalid parameter: max_de cannot be negative.")

    # Mock screen results
    results = [
        {"ticker": "TCS", "company_name": "Tata Consultancy Services", "sector": "IT", "roe": 43.5, "de_ratio": 0.0, "pe": 32.4},
        {"ticker": "INFY", "company_name": "Infosys Ltd", "sector": "IT", "roe": 31.2, "de_ratio": 0.05, "pe": 26.8}
    ]
    return {"count": len(results), "results": results}
