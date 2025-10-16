from __future__ import annotations

from collab_sim.env.simulator import ConversationSimulator
from collab_sim.personas.patient import generate_patient_persona
from collab_sim.personas.clinic import generate_clinic_persona
from collab_sim.scenarios.generator import ScenarioType, generate_scenario
from collab_sim.connectors.stub_client import StubAIServiceClient


def test_patient_journey_booking():
    patient = generate_patient_persona(primary_language="en", seed=10)
    clinic = generate_clinic_persona(seed=11)
    scenario = generate_scenario(scenario_type=ScenarioType.appointment_booking)

    sim = ConversationSimulator(
        patient=patient,
        clinic=clinic,
        scenario=scenario,
        patient_client=StubAIServiceClient(role="patient"),
        clinic_client=StubAIServiceClient(role="clinic", scenario=scenario),
    )

    res = sim.run(max_turns=6)
    assert res.turns == 6
    assert res.total_reward >= 0.0
