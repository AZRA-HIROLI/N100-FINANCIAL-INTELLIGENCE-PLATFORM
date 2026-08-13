import os
import sys
sys.path.append(os.getcwd())

def test_home_page_exists_and_valid():
    assert os.path.exists("pages/01_home.py")
    with open("pages/01_home.py", "r") as f:
        content = f.read()
    assert "Average ROE" in content
    assert "Sector Distribution" in content

def test_profile_page_exists_and_valid():
    assert os.path.exists("pages/02_profile.py")
    with open("pages/02_profile.py", "r") as f:
        content = f.read()
    assert "Ticker not found — please try another" in content
    assert "Investment Thesis Highlights" in content
