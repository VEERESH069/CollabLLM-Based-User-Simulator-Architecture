from __future__ import annotations

from enum import Enum
from typing import Dict, List

from pydantic import BaseModel


class ScenarioType(str, Enum):
    appointment_booking = "appointment_booking"
    follow_up = "follow_up"
    emergency = "emergency"
    complaint = "complaint"


class Scenario(BaseModel):
    type: ScenarioType
    goals: List[str]
    constraints: Dict[str, str]


def generate_scenario(*, scenario_type: ScenarioType) -> Scenario:
    if scenario_type == ScenarioType.appointment_booking:
        return Scenario(
            type=scenario_type,
            goals=["book earliest available appointment", "confirm location"],
            constraints={"insurance": "Aetna", "preferred_doctor": "any"},
        )
    if scenario_type == ScenarioType.follow_up:
        return Scenario(
            type=scenario_type,
            goals=["schedule follow-up", "share lab results"],
            constraints={"preferred_time": "evening"},
        )
    if scenario_type == ScenarioType.emergency:
        return Scenario(
            type=scenario_type,
            goals=["triage and advise immediate action"],
            constraints={"severity": "high"},
        )
    if scenario_type == ScenarioType.complaint:
        return Scenario(
            type=scenario_type,
            goals=["log complaint", "offer resolution"],
            constraints={"topic": "billing"},
        )
    raise ValueError(f"Unsupported scenario type: {scenario_type}")
