from __future__ import annotations

import random
from dataclasses import dataclass

from collabllm_sim.types import ClinicPersona

ROLES = [
    (
        "receptionist",
        ["book_appointment", "reschedule", "collect_demographics"],
        {"formality": "professional", "tone": "neutral"},
    ),
    (
        "nurse",
        ["triage", "collect_vitals", "patient_education"],
        {"formality": "professional", "tone": "empathetic"},
    ),
    (
        "doctor",
        ["diagnose", "prescribe", "order_tests", "follow_up"],
        {"formality": "professional", "tone": "assuring"},
    ),
]


@dataclass(frozen=True)
class ClinicStaff:
    persona: ClinicPersona


def generate_clinic_persona(seed: int | None = None, role: str | None = None) -> ClinicPersona:
    rng = random.Random(seed)
    role_choices = {name: (caps, style) for name, caps, style in ROLES}
    if role is None:
        role = rng.choice(list(role_choices.keys()))
    caps, style = role_choices[role]
    return ClinicPersona(role=role, capabilities=list(caps), style=dict(style))
