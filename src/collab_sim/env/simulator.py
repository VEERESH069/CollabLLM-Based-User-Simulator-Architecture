from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional

from ..personas.patient import PatientPersona
from ..personas.clinic import ClinicPersona
from ..scenarios.generator import Scenario
from ..rewards.multi_turn import RewardResult, compute_rewards
from ..analytics.logger import SimulationLogger


@dataclass
class Turn:
    speaker: str
    text: str


@dataclass
class ConversationResult:
    success: bool
    turns: int
    total_reward: float


class ConversationSimulator:
    def __init__(
        self,
        *,
        patient: PatientPersona,
        clinic: ClinicPersona,
        scenario: Scenario,
        patient_client,
        clinic_client,
        logger: Optional[SimulationLogger] = None,
    ) -> None:
        self.patient = patient
        self.clinic = clinic
        self.scenario = scenario
        self.patient_client = patient_client
        self.clinic_client = clinic_client
        self.logger = logger
        self.turns: List[Turn] = []

    def run(self, *, max_turns: int = 10) -> ConversationResult:
        current_speaker = "patient"
        for _ in range(max_turns):
            if current_speaker == "patient":
                # Initial prompt nudges patient towards scenario goal
                seed_msg = f"scenario={self.scenario.type.value} goals={','.join(self.scenario.goals)}"
                text = self.patient_client.respond(seed_msg, language=self.patient.primary_language)
            else:
                text = self.clinic_client.respond("", language=self.patient.primary_language)

            self.turns.append(Turn(speaker=current_speaker, text=text))
            if self.logger:
                self.logger.log_turn(self.patient, self.clinic, self.scenario, current_speaker, text)

            current_speaker = "clinic" if current_speaker == "patient" else "patient"

        reward: RewardResult = compute_rewards(self.turns, self.scenario)
        if self.logger:
            self.logger.log_summary(self.patient, self.clinic, self.scenario, reward)
        return ConversationResult(success=reward.success, turns=len(self.turns), total_reward=reward.total)
