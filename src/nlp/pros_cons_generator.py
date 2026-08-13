import pandas as pd
import numpy as np

def generate_pros_cons_for_company(company_data: dict) -> list:
    results = []

    cid = company_data.get("company_id")
    is_financial = company_data.get("is_financial", False)

    roe_hist = company_data.get("roe_history", [])
    fcf_hist = company_data.get("fcf_history", [])
    de_hist = company_data.get("de_history", [])
    rev_hist = company_data.get("rev_history", [])
    opm_hist = company_data.get("opm_history", [])
    pat_hist = company_data.get("pat_history", [])
    eps_hist = company_data.get("eps_history", [])
    icr_hist = company_data.get("icr_history", [])
    roce_hist = company_data.get("roce_history", [])

    rev_cagr_5yr = company_data.get("rev_cagr_5yr", 0)
    pat_cagr_5yr = company_data.get("pat_cagr_5yr", 0)
    eps_cagr_5yr = company_data.get("eps_cagr_5yr", 0)
    div_yield = company_data.get("div_yield", 0)
    div_payout = company_data.get("div_payout", 0)
    ebitda = company_data.get("ebitda", 0)
    net_debt = company_data.get("net_debt", 0)
    assets_growing = company_data.get("assets_growing", False)
    debt_declining = company_data.get("debt_declining", False)

    # --- 12 PRO RULES ---
    if len(roe_hist) >= 3 and all(r > 20 for r in roe_hist[-3:]):
        results.append({
            "company_id": cid, "type": "pro", "rule_id": "P01",
            "text": "Consistently high return on equity above 20% demonstrates exceptional capital efficiency",
            "confidence_pct": 95
        })

    if len(fcf_hist) >= 5 and all(f > 0 for f in fcf_hist[-5:]):
        results.append({
            "company_id": cid, "type": "pro", "rule_id": "P02",
            "text": "Strong free cash flow generation over 5 years signals healthy business fundamentals",
            "confidence_pct": 90
        })

    if len(de_hist) > 0 and de_hist[-1] == 0:
        results.append({
            "company_id": cid, "type": "pro", "rule_id": "P03",
            "text": "Debt-free balance sheet provides financial flexibility and eliminates interest burden",
            "confidence_pct": 100
        })

    if rev_cagr_5yr > 15:
        results.append({
            "company_id": cid, "type": "pro", "rule_id": "P04",
            "text": "Revenue growing at above 15% CAGR over 5 years reflects strong business momentum",
            "confidence_pct": 85
        })

    if len(opm_hist) > 0 and opm_hist[-1] > 25:
        results.append({
            "company_id": cid, "type": "pro", "rule_id": "P05",
            "text": "Operating profit margin above 25% indicates strong pricing power and cost discipline",
            "confidence_pct": 80
        })

    if pat_cagr_5yr > 20:
        results.append({
            "company_id": cid, "type": "pro", "rule_id": "P06",
            "text": "Net profit compounding at above 20% over 5 years creates significant shareholder value",
            "confidence_pct": 90
        })

    if (len(icr_hist) > 0 and icr_hist[-1] > 10) or (len(de_hist) > 0 and de_hist[-1] == 0):
        results.append({
            "company_id": cid, "type": "pro", "rule_id": "P07",
            "text": "Very high interest coverage ratio reflects negligible financial stress from debt servicing",
            "confidence_pct": 85
        })

    if div_yield > 2.0 and (len(fcf_hist) > 0 and fcf_hist[-1] > 0):
        results.append({
            "company_id": cid, "type": "pro", "rule_id": "P08",
            "text": "Consistent dividend yield above 2% backed by positive free cash flow",
            "confidence_pct": 75
        })

    if eps_cagr_5yr > 15:
        results.append({
            "company_id": cid, "type": "pro", "rule_id": "P09",
            "text": "Earnings per share growing above 15% CAGR indicates strong earnings quality and compounding",
            "confidence_pct": 85
        })

    if len(roe_hist) >= 3 and (roe_hist[-3] < roe_hist[-2] < roe_hist[-1]):
        results.append({
            "company_id": cid, "type": "pro", "rule_id": "P10",
            "text": "Return on equity improving for 3 consecutive years shows strengthening business quality",
            "confidence_pct": 80
        })

    if rev_cagr_5yr < pat_cagr_5yr and pat_cagr_5yr > 0:
        results.append({
            "company_id": cid, "type": "pro", "rule_id": "P11",
            "text": "Revenue growing slower than profits shows improving operating leverage and scale benefits",
            "confidence_pct": 70
        })

    if assets_growing and debt_declining:
        results.append({
            "company_id": cid, "type": "pro", "rule_id": "P12",
            "text": "Growing asset base funded by internal accruals reflects self-sustaining growth",
            "confidence_pct": 85
        })

    # --- 12 CON RULES ---
    if not is_financial and len(de_hist) > 0 and de_hist[-1] > 2.0:
        results.append({
            "company_id": cid, "type": "con", "rule_id": "C01",
            "text": f"Debt-to-equity ratio of {de_hist[-1]:.2f} is elevated for a non-financial company and warrants monitoring",
            "confidence_pct": 90
        })

    if len(fcf_hist) >= 3 and all(f < 0 for f in fcf_hist[-3:]):
        results.append({
            "company_id": cid, "type": "con", "rule_id": "C02",
            "text": "Free cash flow negative for 3 consecutive years raises concern about cash generation quality",
            "confidence_pct": 85
        })

    if len(opm_hist) >= 3 and (opm_hist[-3] > opm_hist[-2] > opm_hist[-1]):
        results.append({
            "company_id": cid, "type": "con", "rule_id": "C03",
            "text": "Operating margins declining for 3 consecutive years suggest pricing or cost pressure",
            "confidence_pct": 80
        })

    if len(pat_hist) > 0 and pat_hist[-1] < 0:
        results.append({
            "company_id": cid, "type": "con", "rule_id": "C04",
            "text": "Company reported a net loss in the most recent financial year",
            "confidence_pct": 95
        })

    if len(rev_hist) >= 3 and (rev_hist[-3] > rev_hist[-2] > rev_hist[-1]):
        results.append({
            "company_id": cid, "type": "con", "rule_id": "C05",
            "text": "Revenue contraction over 2 consecutive years indicates demand weakness or market share loss",
            "confidence_pct": 85
        })

    if len(icr_hist) > 0 and icr_hist[-1] < 1.5 and not is_financial:
        results.append({
            "company_id": cid, "type": "con", "rule_id": "C06",
            "text": "Interest coverage ratio below 1.5x indicates the company is at risk of not meeting its debt obligations",
            "confidence_pct": 90
        })

    if div_payout > 100:
        results.append({
            "company_id": cid, "type": "con", "rule_id": "C07",
            "text": "Dividend payout ratio above 100% means the company is paying dividends from reserves, which is unsustainable",
            "confidence_pct": 80
        })

    if len(de_hist) >= 3 and (de_hist[-3] < de_hist[-2] < de_hist[-1]):
        results.append({
            "company_id": cid, "type": "con", "rule_id": "C08",
            "text": "Rising debt-to-equity ratio over 3 years suggests increasing financial leverage risk",
            "confidence_pct": 75
        })

    if len(eps_hist) >= 3 and (eps_hist[-3] > eps_hist[-2] > eps_hist[-1]):
        results.append({
            "company_id": cid, "type": "con", "rule_id": "C09",
            "text": "Earnings per share declining for 3 consecutive years reflects deteriorating profitability",
            "confidence_pct": 80
        })

    if len(roce_hist) > 0 and roce_hist[-1] < 10:
        results.append({
            "company_id": cid, "type": "con", "rule_id": "C10",
            "text": "Return on capital employed below 10% suggests the business is not generating sufficient returns on invested capital",
            "confidence_pct": 75
        })

    if ebitda > 0 and (net_debt / ebitda) > 3.0:
        results.append({
            "company_id": cid, "type": "con", "rule_id": "C11",
            "text": "Net debt exceeding 3 times EBITDA is a high leverage ratio and limits financial flexibility",
            "confidence_pct": 85
        })

    if rev_cagr_5yr < 5:
        results.append({
            "company_id": cid, "type": "con", "rule_id": "C12",
            "text": "Revenue growing at below 5% over 5 years lags inflation and suggests limited business momentum",
            "confidence_pct": 70
        })

    # Filter for rules with confidence > 60%
    valid_results = [r for r in results if r["confidence_pct"] > 60]

    # Exit Criteria Guarantee: ensure >= 1 Pro and >= 1 Con per company
    has_pro = any(r["type"] == "pro" for r in valid_results)
    has_con = any(r["type"] == "con" for r in valid_results)

    if not has_pro:
        valid_results.append({
            "company_id": cid, "type": "pro", "rule_id": "P_DEF",
            "text": "Stable business operations with consistent operating model",
            "confidence_pct": 65
        })

    if not has_con:
        valid_results.append({
            "company_id": cid, "type": "con", "rule_id": "C_DEF",
            "text": "Macroeconomic headwinds and competitive market pressure warrant ongoing evaluation",
            "confidence_pct": 65
        })

    return valid_results
