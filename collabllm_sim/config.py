from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


@dataclass
class SimulationConfig:
    patient_service_url: str | None
    clinic_service_url: str | None
    default_language: str
    output_dir: Path
    runs: int
    concurrency: int
    seed: int | None
    max_turns: int
    alpha: float  # weight for task progress
    beta: float   # weight for helpfulness
    gamma: float  # weight for style alignment
    lambda_: float  # penalty weight for safety issues


def load_config(env: os._Environ[str] | dict[str, str] | None = None) -> SimulationConfig:
    # Load .env if present (does not override explicit env vars)
    load_dotenv(override=False)

    if env is None:
        env = os.environ

    output_dir = Path(env.get("SIM_OUTPUT_DIR", "./outputs")).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    return SimulationConfig(
        patient_service_url=env.get("SIM_PATIENT_SERVICE_URL"),
        clinic_service_url=env.get("SIM_CLINIC_SERVICE_URL"),
        default_language=env.get("SIM_LANGUAGE", "en"),
        output_dir=output_dir,
        runs=int(env.get("SIM_RUNS", "10")),
        concurrency=int(env.get("SIM_CONCURRENCY", "1")),
        seed=int(env["SIM_SEED"]) if env.get("SIM_SEED") else None,
        max_turns=int(env.get("SIM_MAX_TURNS", "10")),
        alpha=float(env.get("SIM_REWARD_ALPHA", "0.6")),
        beta=float(env.get("SIM_REWARD_BETA", "0.3")),
        gamma=float(env.get("SIM_REWARD_GAMMA", "0.1")),
        lambda_=float(env.get("SIM_REWARD_LAMBDA", "0.0")),
    )
