from typing import Optional, Tuple

def compute_net_profit_margin(net_profit: float, sales: float):
    if sales is None or sales == 0:
        return None
    return round((net_profit / sales) * 100.0, 2)

def compute_operating_profit_margin(operating_profit: float, sales: float, opm_percentage_source: float = None):
    if sales is None or sales == 0:
        return None
    return round((operating_profit / sales) * 100.0, 2)

def compute_return_on_equity(net_profit: float, equity_capital: float, reserves: float):
    equity_base = (equity_capital or 0.0) + (reserves or 0.0)
    if equity_base <= 0:
        return None
    return round((net_profit / equity_base) * 100.0, 2)

def compute_debt_to_equity(borrowings: float, equity_capital: float, reserves: float, broad_sector: str = ""):
    borrowings = borrowings or 0.0
    equity_base = (equity_capital or 0.0) + (reserves or 0.0)
    if borrowings == 0:
        return 0.0, False
    if equity_base <= 0:
        return None, False
    de_ratio = round(borrowings / equity_base, 2)
    is_financial = broad_sector.upper() in ["FINANCIALS", "FINANCIAL SERVICES", "BANKS", "NBFC"]
    return de_ratio, (de_ratio > 5.0) and not is_financial

def compute_interest_coverage_ratio(operating_profit: float, other_income: float, interest: float):
    operating_profit = operating_profit or 0.0
    other_income = other_income or 0.0
    interest = interest or 0.0
    if interest == 0:
        return None, "Debt Free", False
    ebit = operating_profit + other_income
    icr = round(ebit / interest, 2)
    return icr, str(icr), icr < 1.5

def compute_asset_turnover(sales: float, total_assets: float):
    if total_assets is None or total_assets == 0:
        return None
    return round((sales or 0.0) / total_assets, 2)
