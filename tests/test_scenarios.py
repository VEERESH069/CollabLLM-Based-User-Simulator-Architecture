from collabllm_sim.scenarios.generator import generate_scenario


def test_generate_scenario_types() -> None:
    for s in ["appointment_booking", "follow_up", "emergency", "complaint"]:
        sc = generate_scenario(seed=1, scenario_type=s)
        assert sc.type == s
        assert sc.goal
        assert sc.seed_context
        assert isinstance(sc.constraints, dict)
