from __future__ import annotations

from collab_sim.env.simulator import ConversationSimulator
from collab_sim.personas.patient import generate_patient_persona
from collab_sim.personas.clinic import generate_clinic_persona
from collab_sim.scenarios.generator import ScenarioType, generate_scenario
from collab_sim.connectors.stub_client import StubAIServiceClient


def test_simulation_runs_and_logs(tmp_path):
    patient = generate_patient_persona(seed=1)
    clinic = generate_clinic_persona(seed=2)
    scenario = generate_scenario(scenario_type=ScenarioType.appointment_booking)

    sim = ConversationSimulator(
        patient=patient,
        clinic=clinic,
        scenario=scenario,
        patient_client=StubAIServiceClient(role="patient"),
        clinic_client=StubAIServiceClient(role="clinic", scenario=scenario),
        logger=None,
    )

    res = sim.run(max_turns=4)
    assert res.turns == 4
    assert isinstance(res.total_reward, float)
