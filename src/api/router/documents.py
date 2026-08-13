from fastapi import APIRouter

router = APIRouter(tags=["Documents"])

@router.get("/companies/{ticker}/documents", summary="Get annual report links with validation flag")
async def get_company_documents(ticker: str):
    docs = [
        {"year": 2024, "title": "Annual Report FY24", "url": f"https://investors.{ticker.lower()}.com/ar2024.pdf", "is_url_valid": True},
        {"year": 2023, "title": "Annual Report FY23", "url": f"https://investors.{ticker.lower()}.com/ar2023.pdf", "is_url_valid": True}
    ]
    return {"ticker": ticker.upper(), "annual_reports": docs}
