from fastapi import APIRouter

router = APIRouter(tags=["Valuation"])

@router.get("/market-cap/{ticker}", summary="Get historical valuation multiples 2019-2024")
async def get_valuation_multiples(ticker: str):
    history = [
        {"year": 2019, "pe": 24.1, "pb": 7.2, "ev_ebitda": 18.0, "dividend_yield_pct": 2.1},
        {"year": 2020, "pe": 28.5, "pb": 8.1, "ev_ebitda": 21.4, "dividend_yield_pct": 1.9},
        {"year": 2021, "pe": 34.2, "pb": 10.5, "ev_ebitda": 25.1, "dividend_yield_pct": 1.5},
        {"year": 2022, "pe": 30.0, "pb": 9.0, "ev_ebitda": 22.0, "dividend_yield_pct": 1.8},
        {"year": 2023, "pe": 27.4, "pb": 8.2, "ev_ebitda": 20.1, "dividend_yield_pct": 2.0},
        {"year": 2024, "pe": 31.2, "pb": 9.4, "ev_ebitda": 23.5, "dividend_yield_pct": 1.7}
    ]
    return {"ticker": ticker.upper(), "valuation_history": history}
