import pandas as pd
import numpy as np

def compute_cashflow_kpis(company_id: int, sector: str, df_financials: pd.DataFrame) -> dict:
    cfo_series = df_financials["cfo"].values
    pat_series = df_financials["pat"].values
    sales_series = df_financials["sales"].values
    cfi_series = df_financials.get("cfi", pd.Series([0]*len(df_financials))).values
    cff_series = df_financials.get("cff", pd.Series([0]*len(df_financials))).values
    borrowings_series = df_financials.get("borrowings", pd.Series([0]*len(df_financials))).values

    # CFO Quality Score (5-year average of CFO / PAT)
    with np.errstate(divide='ignore', invalid='ignore'):
        cfo_pat_ratios = np.where(pat_series != 0, cfo_series / pat_series, 0)
    cfo_quality_score = float(np.nanmean(cfo_pat_ratios[-5:]))

    if cfo_quality_score > 1.0:
        cfo_quality_label = "High Quality"
    elif cfo_quality_score >= 0.5:
        cfo_quality_label = "Moderate"
    else:
        cfo_quality_label = "Accrual Risk"

    # CapEx Intensity (Latest year abs(CFI) / Sales * 100)
    latest_sales = sales_series[-1] if sales_series[-1] != 0 else 1.0
    capex_intensity_pct = float((abs(cfi_series[-1]) / latest_sales) * 100)

    if capex_intensity_pct < 3.0:
        capex_label = "Asset Light"
    elif capex_intensity_pct <= 8.0:
        capex_label = "Moderate"
    else:
        capex_label = "Capital Intensive"

    # FCF CAGR 5yr
    fcf_series = cfo_series - abs(cfi_series)
    if len(fcf_series) >= 5 and fcf_series[-5] > 0 and fcf_series[-1] > 0:
        fcf_cagr_5yr = float(((fcf_series[-1] / fcf_series[-5]) ** (1/4) - 1) * 100)
    else:
        fcf_cagr_5yr = 0.0

    # FCF Conversion %
    fcf_conversion_pct = float(cfo_quality_score * 100)

    # Distress Flag: CFO < 0 AND CFF > 0 in latest year
    distress_flag = bool(cfo_series[-1] < 0 and cff_series[-1] > 0)

    # Deleveraging Flag: CFF < 0 AND borrowings declining YoY
    borrowings_declining = len(borrowings_series) >= 2 and borrowings_series[-1] < borrowings_series[-2]
    deleveraging_flag = bool(cff_series[-1] < 0 and borrowings_declining)

    # Capital Allocation Label
    if distress_flag:
        capital_allocation_label = "Distress Signal"
    elif deleveraging_flag:
        capital_allocation_label = "Deleveraging"
    elif capex_intensity_pct > 8.0:
        capital_allocation_label = "Heavy Reinvestor"
    else:
        capital_allocation_label = "Balanced Capital Allocator"

    return {
        "company_id": company_id,
        "sector": sector,
        "cfo_quality_score": round(cfo_quality_score, 2),
        "cfo_quality_label": cfo_quality_label,
        "capex_intensity_pct": round(capex_intensity_pct, 2),
        "capex_label": capex_label,
        "fcf_cagr_5yr": round(fcf_cagr_5yr, 2),
        "fcf_conversion_pct": round(fcf_conversion_pct, 2),
        "distress_flag": distress_flag,
        "deleveraging_flag": deleveraging_flag,
        "capital_allocation_label": capital_allocation_label,
        "latest_cfo": float(cfo_series[-1]),
        "latest_cff": float(cff_series[-1]),
        "latest_pat": float(pat_series[-1])
    }
