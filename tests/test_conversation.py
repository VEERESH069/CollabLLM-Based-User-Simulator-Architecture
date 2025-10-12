import asyncio
from typing import List

from collabllm_sim.conversation.engine import ConversationEngine, RewardModel, RewardWeights
from collabllm_sim.scenarios.generator import generate_scenario
from collabllm_sim.types import Language, TurnEvent


async def _run_once() -> List[TurnEvent]:
    sc = generate_scenario(seed=0, scenario_type="appointment_booking")
    rm = RewardModel(RewardWeights(alpha=0.6, beta=0.3, gamma=0.1, lambda_=0.0))
    engine = ConversationEngine(scenario=sc, max_turns=4, reward_model=rm)
    return await engine.run(run_id="test_run", language=Language.EN)


def test_engine_runs_and_produces_events() -> None:
    try:
        events = asyncio.run(_run_once())
    except RuntimeError:
        loop = asyncio.get_event_loop()
        events = loop.run_until_complete(_run_once())

    assert len(events) == 4
    assert events[0].speaker.value in {"patient", "clinic"}
    assert events[0].language.value in {"en", "ar"}
