import pandas as pd

class DQValidator:
    def __init__(self):
        self.failures = []

    def log_failure(self, rule_id: str, severity: str, table: str, description: str, key_val: str):
        self.failures.append({
            "rule_id": rule_id,
            "severity": severity,
            "table_name": table,
            "description": description,
            "key_value": str(key_val)
        })

    def validate_companies(self, df: pd.DataFrame):
        # DQ-01: Primary Key Uniqueness
        dups = df[df.duplicated('company_id', keep=False)]
        for cid in dups['company_id'].unique():
            self.log_failure("DQ-01", "CRITICAL", "companies", "Duplicate Primary Key", cid)

    def validate_financials(self, df: pd.DataFrame, table_name: str):
        # DQ-02: Composite Primary Key Uniqueness (company_id, year)
        dups = df[df.duplicated(['company_id', 'year'], keep=False)]
        for _, row in dups.iterrows():
            self.log_failure("DQ-02", "CRITICAL", table_name, "Duplicate Composite PK", f"{row['company_id']}-{row['year']}")

        # DQ-04: Balance Sheet Check (<1% Imbalance)
        if table_name == 'balancesheet' and 'total_assets' in df.columns and 'total_liabilities' in df.columns:
            imbalance = df[abs(df['total_assets'] - df['total_liabilities']) / df['total_assets'] > 0.01]
            for _, row in imbalance.iterrows():
                self.log_failure("DQ-04", "WARNING", table_name, "Balance Sheet Imbalance > 1%", f"{row['company_id']}-{row['year']}")

        # DQ-06: Positive Sales Check
        if table_name == 'profitandloss' and 'sales' in df.columns:
            neg_sales = df[df['sales'] <= 0]
            for _, row in neg_sales.iterrows():
                self.log_failure("DQ-06", "WARNING", table_name, "Non-positive Sales value", f"{row['company_id']}-{row['year']}")

    def save_report(self, filepath: str = "output/validation_failures.csv"):
        report_df = pd.DataFrame(self.failures)
        report_df.to_csv(filepath, index=False)
        return report_df
