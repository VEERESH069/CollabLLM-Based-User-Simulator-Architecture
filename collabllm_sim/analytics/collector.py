from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path

import orjson

from collabllm_sim.types import TurnEvent


@dataclass
class AnalyticsCollector:
    output_dir: Path

    def write_jsonl(self, run_id: str, events: Iterable[TurnEvent]) -> Path:
        run_path = self.output_dir / f"{run_id}.jsonl"
        with run_path.open("wb") as f:
            for e in events:
                line = orjson.dumps(
                    {
                        "run_id": e.run_id,
                        "turn": e.turn,
                        "speaker": e.speaker.value,
                        "text": e.text,
                        "language": e.language.value,
                        "state": e.state,
                        "rewards": e.rewards,
                    }
                )
                f.write(line + b"\n")
        return run_path

    def summarize(self, runs: Iterable[list[TurnEvent]]) -> dict[str, float]:
        total_conversations = 0
        total_turns = 0
        total_reward = 0.0
        for events in runs:
            total_conversations += 1
            total_turns += len(events)
            total_reward += sum(e.rewards.get("task_progress", 0) for e in events)
        if total_conversations == 0:
            return {"conversations": 0, "avg_turns": 0.0, "avg_reward": 0.0}
        return {
            "conversations": float(total_conversations),
            "avg_turns": total_turns / total_conversations,
            "avg_reward": total_reward / total_conversations,
        }
