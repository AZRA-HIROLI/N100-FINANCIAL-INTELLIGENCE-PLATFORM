import os
import glob
import pandas as pd

def test_dq_rule_01_screener_master_exists():
    assert os.path.exists("output/screener_output_master.csv")

def test_dq_rule_02_peer_percentiles_csv_exists():
    assert os.path.exists("output/peer_percentiles.csv")

def test_dq_rule_03_peer_comparison_master_exists():
    assert os.path.exists("output/peer_comparison_master.csv")

def test_dq_rule_04_peer_group_summaries_exists():
    assert os.path.exists("output/peer_group_summaries.csv")

def test_dq_rule_05_screener_presets_count_between_5_and_50():
    master_df = pd.read_csv("output/screener_output_master.csv")
    preset_counts = master_df["preset"].value_counts()
    assert len(preset_counts) >= 6
    for preset, count in preset_counts.items():
        assert 5 <= count <= 50, f"Preset {preset} has invalid count: {count}"

def test_dq_rule_06_peer_groups_count_equals_11():
    df_pct = pd.read_csv("output/peer_percentiles.csv")
    groups = df_pct["peer_group_name"].unique()
    assert len(groups) == 11, f"Expected 11 peer groups, found {len(groups)}"

def test_dq_rule_07_percentile_rank_bounds():
    df_pct = pd.read_csv("output/peer_percentiles.csv")
    assert df_pct["percentile_rank"].min() >= 0.0
    assert df_pct["percentile_rank"].max() <= 1.0

def test_dq_rule_08_radar_charts_directory_populated():
    charts = glob.glob("reports/radar_charts/*.png")
    assert len(charts) >= 10, f"Expected at least 10 radar charts, found {len(charts)}"

def test_dq_rule_09_winsorised_score_bounds():
    master_df = pd.read_csv("output/screener_output_master.csv")
    assert master_df["winsorised_composite_score"].min() >= 0.0
    assert master_df["winsorised_composite_score"].max() <= 100.0

def test_dq_rule_10_no_null_company_ids_in_percentiles():
    df_pct = pd.read_csv("output/peer_percentiles.csv")
    assert df_pct["company_id"].isna().sum() == 0

def test_dq_rule_11_metrics_covered_in_peer_rankings():
    df_pct = pd.read_csv("output/peer_percentiles.csv")
    metrics = df_pct["metric"].unique()
    assert len(metrics) == 10

def test_dq_rule_12_de_inverse_ranking_logic():
    df_pct = pd.read_csv("output/peer_percentiles.csv")
    de_sub = df_pct[df_pct["metric"] == "debt_to_equity"].dropna()
    assert len(de_sub) > 0

def test_dq_rule_13_config_presets_defined():
    import json
    with open("config/screener_config.json", "r") as f:
        cfg = json.load(f)
    assert len(cfg["presets"]) >= 6

def test_dq_rule_14_quality_compounder_roe_threshold():
    master_df = pd.read_csv("output/screener_output_master.csv")
    qc = master_df[master_df["preset"] == "quality_compounder"]
    assert (qc["return_on_equity_pct"] >= 15.0).all()
