from __future__ import annotations

import asyncio
import uuid
from typing import Any

import typer
from rich import print as rprint

from collabllm_sim.analytics.collector import AnalyticsCollector
from collabllm_sim.config import SimulationConfig, load_config
from collabllm_sim.conversation.engine import ConversationEngine, RewardModel, RewardWeights
from collabllm_sim.scenarios.generator import generate_scenario
from collabllm_sim.types import Language

app = typer.Typer(add_completion=False)

SCENARIO_OPTION = typer.Option(
    "appointment_booking",
    help="Scenario type: appointment_booking|follow_up|emergency|complaint",
)
RUNS_OPTION = typer.Option(None, help="Override number of runs (else SIM_RUNS)")
LANGUAGE_OPTION = typer.Option(Language.EN, help="en or ar")
MAX_TURNS_OPTION = typer.Option(None, help="Override max turns (else SIM_MAX_TURNS)")


@app.command()
def run(
    scenario: str = SCENARIO_OPTION,
    runs: int | None = RUNS_OPTION,
    language: Language = LANGUAGE_OPTION,
    max_turns: int | None = MAX_TURNS_OPTION,
) -> None:
    """Run a batch of simulated conversations and write JSONL logs."""
    config: SimulationConfig = load_config()
    if runs is not None:
        config.runs = runs
    if max_turns is not None:
        config.max_turns = max_turns

    reward = RewardModel(RewardWeights(
        alpha=config.alpha, beta=config.beta, gamma=config.gamma, lambda_=config.lambda_
    ))

    async def _one_run(i: int) -> list[Any]:
        sc = generate_scenario(seed=(config.seed or 0) + i, scenario_type=scenario)
        engine = ConversationEngine(scenario=sc, max_turns=config.max_turns, reward_model=reward)
        return await engine.run(run_id=str(uuid.uuid4()), language=language)

    async def _main() -> None:
        runs_events: list[list[Any]] = []
        sem = asyncio.Semaphore(config.concurrency)

        async def _guarded(i: int) -> None:
            async with sem:
                events = await _one_run(i)
                runs_events.append(events)

        await asyncio.gather(*[_guarded(i) for i in range(config.runs)])

        collector = AnalyticsCollector(config.output_dir)
        for evs in runs_events:
            collector.write_jsonl(evs[0].run_id, evs)
        summary = collector.summarize(runs_events)
        rprint({"summary": summary, "output_dir": str(config.output_dir)})

    try:
        asyncio.run(_main())
    except RuntimeError:
        # Fallback for environments with existing event loop
        loop = asyncio.get_event_loop()
        loop.run_until_complete(_main())


def main() -> None:
    app()


if __name__ == "__main__":
    main()
