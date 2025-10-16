from __future__ import annotations

from collab_sim.personas.patient import generate_patient_persona
from collab_sim.personas.clinic import generate_clinic_persona


def test_generate_patient_persona_variety():
    p1 = generate_patient_persona(seed=42)
    p2 = generate_patient_persona(seed=43)
    assert p1.name != p2.name or p1.age != p2.age
    assert p1.primary_language in {"en", "ar", "bilingual"}


def test_generate_clinic_persona():
    c = generate_clinic_persona(seed=42)
    assert c.role in {"receptionist", "nurse", "doctor"}
