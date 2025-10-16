from collabllm_sim.personas.generator import generate_patient_persona
from collabllm_sim.types import Language


def test_generate_patient_persona_basic() -> None:
    p = generate_patient_persona(seed=42)
    assert p.id
    assert 18 <= p.demographics.age <= 85
    assert p.demographics.nationality in {"UAE", "IN", "PK", "PH", "UK", "US", "EG", "SA"}
    assert p.demographics.language in {Language.EN, Language.AR}
    assert p.communication_style.brevity in {"short", "medium", "long"}
