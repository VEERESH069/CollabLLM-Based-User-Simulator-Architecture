from __future__ import annotations

import random
import uuid

from collabllm_sim.types import CommunicationStyle, Demographics, Language, PatientPersona


def generate_patient_persona(seed: int | None = None, language: Language | None = None) -> PatientPersona:
    rng = random.Random(seed)

    demographics = Demographics(
        age=rng.randint(18, 85),
        gender=rng.choice(["male", "female"]),
        nationality=rng.choice(["UAE", "IN", "PK", "PH", "UK", "US", "EG", "SA"]),
        language=language or rng.choice([Language.EN, Language.AR]),
    )

    conditions_pool: list[str] = [
        "type2_diabetes",
        "hypertension",
        "asthma",
        "hyperlipidemia",
        "anxiety",
        "hypothyroidism",
        "back_pain",
        "migraine",
    ]
    num_conditions = rng.choices([0, 1, 2], weights=[0.2, 0.5, 0.3])[0]
    conditions = rng.sample(conditions_pool, k=num_conditions)

    style = CommunicationStyle(
        brevity=rng.choice(["short", "medium", "long"]),
        formality=rng.choice(["casual", "polite", "professional"]),
        tone=rng.choice(["neutral", "anxious", "friendly", "assertive"]),
    )

    return PatientPersona(
        id=str(uuid.uuid4()),
        demographics=demographics,
        conditions=conditions,
        communication_style=style,
    )
