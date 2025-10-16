from __future__ import annotations

import random
from typing import Literal, Optional

from pydantic import BaseModel


ClinicRole = Literal["receptionist", "nurse", "doctor"]


class ClinicPersona(BaseModel):
    name: str
    role: ClinicRole
    department: str


NAMES = [
    "Rashid",
    "Mariam",
    "Khalid",
    "Sara",
    "Ibrahim",
    "Nadia",
]
DEPARTMENTS = [
    "General Practice",
    "Cardiology",
    "Endocrinology",
    "Pediatrics",
    "Neurology",
    "Orthopedics",
]


def generate_clinic_persona(*, seed: Optional[int] = None) -> ClinicPersona:
    rng = random.Random(seed)
    name = rng.choice(NAMES)
    role = rng.choice(["receptionist", "nurse", "doctor"])  # type: ignore[assignment]
    department = rng.choice(DEPARTMENTS)
    return ClinicPersona(name=name, role=role, department=department)
