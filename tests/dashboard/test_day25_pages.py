import os
import sys
sys.path.append(os.getcwd())

def test_all_8_pages_exist():
    expected_pages = [
        "pages/01_home.py", "pages/02_profile.py", "pages/03_screener.py",
        "pages/04_peers.py", "pages/05_trends.py", "pages/06_sectors.py",
        "pages/07_capital.py", "pages/08_reports.py"
    ]
    for p in expected_pages:
        assert os.path.exists(p), f"Missing page file: {p}"

def test_reports_page_badge():
    with open("pages/08_reports.py", "r") as f:
        content = f.read()
    assert "Report unavailable" in content
