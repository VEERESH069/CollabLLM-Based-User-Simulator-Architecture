from __future__ import annotations

import random

from collabllm_sim.types import Scenario


def generate_scenario(seed: int | None = None, scenario_type: str | None = None) -> Scenario:
    rng = random.Random(seed)

    scenario_type = scenario_type or rng.choice(
        ["appointment_booking", "follow_up", "emergency", "complaint"]
    )

    if scenario_type == "appointment_booking":
        goal = "book next available department appointment"
        constraints: dict[str, object] = {
            "preferred_window_days": rng.choice([3, 7, 14]),
            "department": rng.choice(["cardiology", "dermatology", "gp", "orthopedics"]),
            "clinic": rng.choice(["Downtown", "Marina", "International City"]),
        }
        seed_context = "patient has a new symptom and wants earliest suitable slot"

    elif scenario_type == "follow_up":
        goal = "schedule follow-up with same doctor"
        constraints = {"window_days": rng.choice([7, 14, 30])}
        seed_context = "patient had a test and needs to discuss results"

    elif scenario_type == "emergency":
        goal = "triage and suggest ER or urgent slot"
        constraints = {"urgency": rng.choice(["high", "critical"]) }
        seed_context = "patient reports severe acute symptoms"

    else:  # complaint
        goal = "collect complaint details and escalate"
        constraints = {"channel": rng.choice(["email", "call", "in_person"]) }
        seed_context = "patient dissatisfied with previous visit"

    return Scenario(type=scenario_type, goal=goal, constraints=constraints, seed_context=seed_context)
