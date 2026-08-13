PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS stock_prices;
DROP TABLE IF EXISTS financial_ratios;
DROP TABLE IF EXISTS analysis;
DROP TABLE IF EXISTS documents;
DROP TABLE IF EXISTS prosandcons;
DROP TABLE IF EXISTS peer_groups;
DROP TABLE IF EXISTS sectors;
DROP TABLE IF EXISTS cashflow;
DROP TABLE IF EXISTS balancesheet;
DROP TABLE IF EXISTS profitandloss;
DROP TABLE IF EXISTS companies;

CREATE TABLE companies (
    company_id INTEGER PRIMARY KEY,
    ticker TEXT UNIQUE NOT NULL,
    company_name TEXT NOT NULL,
    sector_id INTEGER
);

CREATE TABLE profitandloss (
    company_id INTEGER,
    year INTEGER,
    sales REAL,
    operating_profit REAL,
    opm_percent REAL,
    net_profit REAL,
    eps REAL,
    PRIMARY KEY (company_id, year),
    FOREIGN KEY (company_id) REFERENCES companies(company_id) ON DELETE CASCADE
);

CREATE TABLE balancesheet (
    company_id INTEGER,
    year INTEGER,
    total_assets REAL,
    total_liabilities REAL,
    equity_capital REAL,
    reserves REAL,
    PRIMARY KEY (company_id, year),
    FOREIGN KEY (company_id) REFERENCES companies(company_id) ON DELETE CASCADE
);

CREATE TABLE cashflow (
    company_id INTEGER,
    year INTEGER,
    operating_cash_flow REAL,
    investing_cash_flow REAL,
    financing_cash_flow REAL,
    net_cash_flow REAL,
    PRIMARY KEY (company_id, year),
    FOREIGN KEY (company_id) REFERENCES companies(company_id) ON DELETE CASCADE
);

CREATE TABLE stock_prices (
    company_id INTEGER,
    trade_date TEXT,
    close_price REAL,
    volume INTEGER,
    PRIMARY KEY (company_id, trade_date),
    FOREIGN KEY (company_id) REFERENCES companies(company_id) ON DELETE CASCADE
);

CREATE TABLE financial_ratios (
    company_id INTEGER,
    year INTEGER,
    pe_ratio REAL,
    roe_percent REAL,
    roce_percent REAL,
    PRIMARY KEY (company_id, year),
    FOREIGN KEY (company_id) REFERENCES companies(company_id) ON DELETE CASCADE
);

CREATE TABLE analysis (
    company_id INTEGER PRIMARY KEY,
    analysis_text TEXT,
    FOREIGN KEY (company_id) REFERENCES companies(company_id) ON DELETE CASCADE
);

CREATE TABLE documents (
    doc_id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id INTEGER,
    doc_type TEXT,
    doc_url TEXT,
    FOREIGN KEY (company_id) REFERENCES companies(company_id) ON DELETE CASCADE
);

CREATE TABLE prosandcons (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id INTEGER,
    type TEXT CHECK(type IN ('PRO', 'CON')),
    statement TEXT,
    FOREIGN KEY (company_id) REFERENCES companies(company_id) ON DELETE CASCADE
);

CREATE TABLE peer_groups (
    company_id INTEGER,
    peer_company_id INTEGER,
    PRIMARY KEY (company_id, peer_company_id),
    FOREIGN KEY (company_id) REFERENCES companies(company_id) ON DELETE CASCADE
);
