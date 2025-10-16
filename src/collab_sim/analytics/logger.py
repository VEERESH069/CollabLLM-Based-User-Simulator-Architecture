from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict

from ..personas.patient import PatientPersona
from ..personas.clinic import ClinicPersona
from ..scenarios.generator import Scenario
from ..rewards.multi_turn import RewardResult


@dataclass
class LogTurn:
    timestamp: str
    patient_name: str
    clinic_role: str
    scenario: str
    speaker: str
    text: str


@dataclass
class LogSummary:
    timestamp: str
    patient_name: str
    clinic_role: str
    scenario: str
    success: bool
    total_reward: float
    components: Dict[str, float]


class SimulationLogger:
    def __init__(self, path: Path):
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def _write(self, record: Dict[str, Any]) -> None:
        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

    def log_turn(
        self,
        patient: PatientPersona,
        clinic: ClinicPersona,
        scenario: Scenario,
        speaker: str,
        text: str,
    ) -> None:
        rec = LogTurn(
            timestamp=datetime.utcnow().isoformat(),
            patient_name=patient.name,
            clinic_role=clinic.role,
            scenario=scenario.type.value,
            speaker=speaker,
            text=text,
        )
        self._write({"type": "turn", **asdict(rec)})

    def log_summary(
        self,
        patient: PatientPersona,
        clinic: ClinicPersona,
        scenario: Scenario,
        reward: RewardResult,
    ) -> None:
        rec = LogSummary(
            timestamp=datetime.utcnow().isoformat(),
            patient_name=patient.name,
            clinic_role=clinic.role,
            scenario=scenario.type.value,
            success=reward.success,
            total_reward=reward.total,
            components=reward.components,
        )
        self._write({"type": "summary", **asdict(rec)})
