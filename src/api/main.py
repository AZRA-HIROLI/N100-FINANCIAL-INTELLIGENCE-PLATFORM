import time
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import json

from src.api.routers import (
    companies, screener, sectors, peers, valuation, portfolio, documents, health
)

app = FastAPI(
    title="Financial Intelligence API",
    description="REST API for 92-Company Financial Analytics, Screener, and PDF Reports",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix="/api/v1")
app.include_router(companies.router, prefix="/api/v1")
app.include_router(screener.router, prefix="/api/v1")
app.include_router(sectors.router, prefix="/api/v1")
app.include_router(peers.router, prefix="/api/v1")
app.include_router(valuation.router, prefix="/api/v1")
app.include_router(portfolio.router, prefix="/api/v1")
app.include_router(documents.router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "Financial Intelligence API is active."}
