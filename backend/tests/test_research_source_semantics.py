from app.services.research.source_semantics import (
    can_infer_agent_behavior,
    assert_agent_behavior_source,
)


def test_only_human_behavior_can_infer_agent_behavior():
    assert can_infer_agent_behavior("human_behavior") is True
    assert can_infer_agent_behavior("algorithmic_process") is False
    assert can_infer_agent_behavior("world_state") is False
    assert can_infer_agent_behavior("world_rule") is False
    assert can_infer_agent_behavior("observed_event") is False


def test_remanejamento_style_algorithmic_source_fails_closed():
    try:
        assert_agent_behavior_source("algorithmic_process")
    except ValueError as exc:
        assert "cannot be used" in str(exc)
    else:
        raise AssertionError("algorithmic source was incorrectly accepted")
