from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/sectors", tags=["Sectors"])

@router.get("", summary="Get all 11 sectors summary medians")
async def get_sectors():
    sectors = [
        {"sector": "IT", "company_count": 12, "median_roe": 28.5, "median_pe": 29.1, "median_de": 0.02},
        {"sector": "Banking", "company_count": 14, "median_roe": 15.2, "median_pe": 16.4, "median_de": 6.5}
    ]
    return {"sectors": sectors}

@router.get("/{sector}/companies", summary="Get all companies in a specific sector")
async def get_sector_companies(sector: str):
    s_upper = sector.upper()
    if s_upper not in ["IT", "BANKING", "PHARMA", "ENERGY"]:
        raise HTTPException(status_code=404, detail=f"Sector '{sector}' not found.")
    return {"sector": s_upper, "companies": [{"ticker": "TCS", "roe": 43.5}, {"ticker": "WIPRO", "roe": 18.2}]}
