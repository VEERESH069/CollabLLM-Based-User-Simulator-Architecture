from __future__ import annotations

import random
from typing import List, Literal, Optional

from pydantic import BaseModel, Field


Gender = Literal["male", "female", "other"]
Language = Literal["en", "ar", "bilingual"]
CommunicationStyle = Literal["direct", "indirect", "formal", "casual"]
TechLiteracy = Literal["low", "medium", "high"]


class PatientPersona(BaseModel):
    name: str
    age: int = Field(ge=0, le=110)
    gender: Gender
    location: str
    nationality: str
    primary_language: Language
    conditions: List[str]
    communication_style: CommunicationStyle
    tech_literacy: TechLiteracy


ARAB_NAMES = [
    "Ahmed",
    "Fatima",
    "Omar",
    "Aisha",
    "Hassan",
    "Leila",
    "Yousef",
    "Noor",
]
EN_NAMES = [
    "John",
    "Mary",
    "Alex",
    "Sophia",
    "Michael",
    "Emily",
]
UAE_CITIES = ["Dubai", "Abu Dhabi", "Sharjah", "Ajman", "Al Ain"]
NATIONALITIES = ["UAE", "Egypt", "India", "Pakistan", "Philippines", "UK"]
CONDITIONS = [
    "diabetes",
    "hypertension",
    "asthma",
    "pregnancy",
    "migraine",
    "flu",
    "back pain",
]


def _rand_choice(rng: random.Random, values: List[str]) -> str:
    return values[rng.randrange(0, len(values))]


def generate_patient_persona(
    *, primary_language: Optional[Language] = None, seed: Optional[int] = None
) -> PatientPersona:
    rng = random.Random(seed)
    language = primary_language or rng.choice(["en", "ar", "bilingual"])  # type: ignore[arg-type]
    name_pool = ARAB_NAMES if language == "ar" else EN_NAMES
    name = _rand_choice(rng, name_pool)

    gender = rng.choice(["male", "female"])  # type: ignore[assignment]
    age = rng.randint(18, 85)
    location = _rand_choice(rng, UAE_CITIES)
    nationality = _rand_choice(rng, NATIONALITIES)

    # 0-2 conditions out of pool
    num_conditions = rng.choice([0, 1, 2, 2, 1])
    conditions = rng.sample(CONDITIONS, k=num_conditions)

    communication_style = rng.choice(["direct", "indirect", "formal", "casual"])  # type: ignore[assignment]
    tech_literacy = rng.choice(["low", "medium", "high"])  # type: ignore[assignment]

    return PatientPersona(
        name=name,
        age=age,
        gender=gender,
        location=location,
        nationality=nationality,
        primary_language=language,  # type: ignore[arg-type]
        conditions=conditions,
        communication_style=communication_style,  # type: ignore[arg-type]
        tech_literacy=tech_literacy,  # type: ignore[arg-type]
    )
