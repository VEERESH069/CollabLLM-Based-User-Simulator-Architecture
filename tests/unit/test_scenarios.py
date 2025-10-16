from __future__ import annotations

from collab_sim.scenarios.generator import ScenarioType, generate_scenario


def test_generate_scenarios_all_types():
    for t in ScenarioType:
        s = generate_scenario(scenario_type=t)
        assert s.type == t
        assert len(s.goals) >= 1
