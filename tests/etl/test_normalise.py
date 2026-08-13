import pytest

def normalize_year(val):
    if not val:
        return None
    val_str = str(val).strip()
    if len(val_str) == 4 and val_str.isdigit():
        return f"{val_str}-03"
    if "-" in val_str:
        parts = val_str.split("-")
        if len(parts[0]) == 4:
            return f"{parts[0]}-{parts[1].zfill(2)}"
    return val_str

@pytest.mark.parametrize("input_val, expected", [
    ("2024", "2024-03"),
    (2023, "2023-03"),
    ("2022-03", "2022-03"),
    ("2025-3", "2025-03"),
    ("  2021  ", "2021-03"),
    ("2020-12", "2020-12"),
    (None, None),
    ("", None),
    ("FY24", "FY24"),
    ("2019-Q1", "2019-Q1"),
    ("2018/03", "2018/03"),
    ("2017.3", "2017.3"),
    ("2016-09", "2016-09"),
    ("2015-1", "2015-01"),
    ("1999", "1999-03"),
    ("2030-06", "2030-06"),
    ("abc", "abc"),
    ("2024-03-31", "2024-03-31"),
    ("0000", "0000-03"),
    ("202", "202")
])
def test_normalize_year(input_val, expected):
    assert normalize_year(input_val) == expected
