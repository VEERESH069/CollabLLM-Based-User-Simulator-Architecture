from collabllm_sim.personas.clinic import generate_clinic_persona


def test_generate_clinic_persona_defaults() -> None:
    p = generate_clinic_persona(seed=123)
    assert p.role in {"receptionist", "nurse", "doctor"}
    assert isinstance(p.capabilities, list)
    assert isinstance(p.style, dict)


def test_generate_clinic_persona_specific_role() -> None:
    p = generate_clinic_persona(seed=123, role="doctor")
    assert p.role == "doctor"
    assert "diagnose" in p.capabilities
