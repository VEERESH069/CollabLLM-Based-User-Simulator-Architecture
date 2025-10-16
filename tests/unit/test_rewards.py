from __future__ import annotations

from collab_sim.rewards.multi_turn import compute_rewards
from collab_sim.scenarios.generator import ScenarioType, generate_scenario
from collab_sim.env.simulator import Turn


def test_reward_components_and_success():
    scenario = generate_scenario(scenario_type=ScenarioType.appointment_booking)
    turns = [
        Turn(speaker="patient", text="I want to book an appointment. Please share time."),
        Turn(speaker="clinic", text="Please share your preferred time and location."),
        Turn(speaker="patient", text="Tomorrow morning, thank you!"),
    ]
    res = compute_rewards(turns, scenario)
    assert 0.0 <= res.components["task_completion"] <= 1.0
    assert 0.0 <= res.components["satisfaction"] <= 1.0
    assert 0.0 <= res.components["efficiency"] <= 1.0
    assert res.total >= 0.0
    assert res.success is True
