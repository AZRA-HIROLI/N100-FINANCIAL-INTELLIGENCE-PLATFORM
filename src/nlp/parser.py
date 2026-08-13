import re
import pandas as pd
from typing import Tuple, List

REGEX_PATTERN = r"(\d+)\s*Years?:?\s*([\d.]+)%"

def parse_analysis_text(df_text: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    parsed_records = []
    failures = []

    for idx, row in df_text.iterrows():
        cid = row.get("company_id", idx + 1)
        metric_type = row.get("metric_type", "growth")
        text_val = str(row.get("text_content", ""))

        matches = re.findall(REGEX_PATTERN, text_val, re.IGNORECASE)
        if matches:
            for period, value in matches:
                parsed_records.append({
                    "company_id": int(cid),
                    "metric_type": metric_type,
                    "period_years": int(period),
                    "value_pct": float(value)
                })
        else:
            failures.append({
                "company_id": int(cid),
                "metric_type": metric_type,
                "raw_text": text_val
            })

    return pd.DataFrame(parsed_records), pd.DataFrame(failures)
