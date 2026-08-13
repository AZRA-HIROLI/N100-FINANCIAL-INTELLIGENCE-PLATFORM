import os
import sys
sys.path.append(os.getcwd())

def test_screener_page_exists_and_valid():
    assert os.path.exists("pages/03_screener.py")
    with open("pages/03_screener.py", "r") as f:
        content = f.read()
    assert "Quality Compounder" in content
    assert "Download Screener Results CSV" in content

def test_peers_page_exists_and_valid():
    assert os.path.exists("pages/04_peers.py")
    with open("pages/04_peers.py", "r") as f:
        content = f.read()
    assert "Scatterpolar" in content
    assert "Side-by-Side Peer Metric Comparison Table" in content
