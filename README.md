{
  "metadata": {
    "kernelspec": {
      "name": "python",
      "display_name": "Python (Pyodide)",
      "language": "python"
    },
    "language_info": {
      "codemirror_mode": {
        "name": "python",
        "version": 3
      },
      "file_extension": ".py",
      "mimetype": "text/x-python",
      "name": "python",
      "nbconvert_exporter": "python",
      "pygments_lexer": "ipython3",
      "version": "3.8"
    }
  },
  "nbformat_minor": 5,
  "nbformat": 4,
  "cells": [
    {
      "id": "632fa7a0-6934-4472-9573-c71c44c2bedc",
      "cell_type": "markdown",
      "source": "\n\nimport os\nimport sys\n\nos.makedirs(\"docs\", exist_ok=True)\n\n# 1. Generate comprehensive architecture & reference markdown\narchitecture_md_content = \"\"\"# Financial Intelligence API — System Architecture & Reference\n\n## Overview\nThe Financial Intelligence API is a high-performance backend built on **FastAPI** designed to serve financial analytics, screener queries, peer comparisons, valuation histories, and automated PDF report downloads for 92 tracked companies across 11 sectors.\n\n---\n\n## Directory Structure\n```text\n├── data/                 # SQLite database & local storage\n├── docs/                 # OpenAPI specification (openapi.json) & architecture notes\n├── output/               # Reports, CSV statistics, performance logs\n├── reports/              # Visualizations, heatmaps, test reports, PDF tearsheets\n├── src/                  # Core application source code\n│   ├── api/              # FastAPI application layer\n│   │   ├── routers/      # Modular endpoints (companies, screener, sectors, etc.)\n│   │   └── main.py       # FastAPI application entrypoint & middleware configuration\n│   └── etl/              # Data ingestion, cleaning, and normalization logic\n├── tests/                # Comprehensive test suite (ETL, KPI, DQ, API)\n└── README.md\n\n```\n\n---\n\n## Core API Endpoints Reference\n\n| Endpoint | Method | Description |\n| --- | --- | --- |\n| `/api/v1/health` | `GET` | System health check, uptime, and database row counts |\n| `/api/v1/companies` | `GET` | List all companies with sector and market cap filters |\n| `/api/v1/companies/{ticker}` | `GET` | Full financial and fundamental profile for a given company |\n| `/api/v1/companies/{ticker}/pl` | `GET` | Historical Profit & Loss statement array |\n| `/api/v1/companies/{ticker}/bs` | `GET` | Historical Balance Sheet statement array |\n| `/api/v1/companies/{ticker}/cashflow` | `GET` | Historical Cash Flow statement array |\n| `/api/v1/companies/{ticker}/ratios` | `GET` | Computed financial KPIs (OPM, NPM, D/E) per year |\n| `/api/v1/companies/{ticker}/tearsheet` | `GET` | Download pre-generated company PDF tearsheet |\n| `/api/v1/screener` | `GET` | Parameterized multi-factor financial screener |\n| `/api/v1/sectors` | `GET` | Sector summary statistics and medians |\n| `/api/v1/sectors/{sector}/companies` | `GET` | Constituent companies within a specific sector |\n| `/api/v1/peers/{group_name}` | `GET` | Peer group percentile rankings |\n| `/api/v1/companies/{ticker}/peers/compare` | `GET` | Multi-axis radar comparison data against peer average |\n| `/api/v1/market-cap/{ticker}` | `GET` | Historical valuation multiples (P/E, P/B, EV/EBITDA) |\n| `/api/v1/portfolio/stats` | `GET` | Portfolio-wide P10–P90 percentile breakdown |\n| `/api/v1/companies/{ticker}/documents` | `GET` | Verified annual report links and documentation metadata |\n\n---\n\n## Interactive Documentation\n\n* **Swagger UI:** `http://localhost:8000/docs`\n* **ReDoc UI:** `http://localhost:8000/redoc`\n* **OpenAPI Schema:** Exported to `docs/openapi.json`\n\"\"\"\n\nwith open(\"docs/architecture.md\", \"w\") as f:\nf.write(architecture_md_content)\n\nprint(\"=== Day 44 Execution Complete ===\")\nprint(\"Generated Architecture Documentation: docs/architecture.md\")\n\n```\n\n```",
      "metadata": {}
    },
    {
      "id": "2d2fd2ee-65b5-4682-aa07-f5842f8ad5b8",
      "cell_type": "code",
      "source": "",
      "metadata": {
        "trusted": true
      },
      "outputs": [],
      "execution_count": null
    }
  ]
}
