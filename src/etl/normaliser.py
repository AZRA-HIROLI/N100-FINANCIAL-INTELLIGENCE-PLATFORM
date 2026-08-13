import re
import pandas as pd

def normalize_ticker(ticker: str) -> str:
    """Cleans ticker string: converts to uppercase, strips spaces, removes exchange extensions."""
    if not isinstance(ticker, str):
        return ""
    cleaned = ticker.strip().upper()
    cleaned = re.sub(r'[\.\-\_]?(NS|BO|EQ)$', '', cleaned)
    return cleaned

def normalize_year(val) -> int:
    """Extracts 4-digit fiscal year from various raw inputs (e.g., 'FY2023', '2022-23', 'Mar-19')."""
    if pd.isna(val):
        return None
    val_str = str(val).strip()
    match = re.search(r'(20\d{2})', val_str)
    if match:
        return int(match.group(1))
    return None
