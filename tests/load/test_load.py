from __future__ import annotations

import concurrent.futures as cf

from collab_sim.env.simulator import ConversationSimulator
from collab_sim.personas.patient import generate_patient_persona
from collab_sim.personas.clinic import generate_clinic_persona
from collab_sim.scenarios.generator import ScenarioType, generate_scenario
from collab_sim.connectors.stub_client import StubAIServiceClient


def _run_one(seed: int) -> float:
    patient = generate_patient_persona(seed=seed)
    clinic = generate_clinic_persona(seed=seed + 1)
    scenario = generate_scenario(scenario_type=ScenarioType.appointment_booking)
    sim = ConversationSimulator(
        patient=patient,
        clinic=clinic,
        scenario=scenario,
        patient_client=StubAIServiceClient(role="patient"),
        clinic_client=StubAIServiceClient(role="clinic", scenario=scenario),
    )
    return sim.run(max_turns=4).total_reward


def test_concurrent_users():
    seeds = list(range(50))
    with cf.ThreadPoolExecutor(max_workers=10) as ex:
        rewards = list(ex.map(_run_one, seeds))
    assert len(rewards) == len(seeds)
