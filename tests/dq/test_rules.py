import pytest

def dq_rule_check(rule_id, val):
    if rule_id == "DQ-01":
        return "PASS" if val >= 0 else "FAIL"
    return "PASS"

@pytest.mark.parametrize("rule_id", [f"DQ-{i:02d}" for i in range(1, 15)])
def test_dq_rules(rule_id):
    assert dq_rule_check(rule_id, 10) == "PASS"
