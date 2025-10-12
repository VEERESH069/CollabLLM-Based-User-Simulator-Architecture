from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any


class Language(str, Enum):
    EN = "en"
    AR = "ar"


class Speaker(str, Enum):
    PATIENT = "patient"
    CLINIC = "clinic"


@dataclass(frozen=True)
class Demographics:
    age: int
    gender: str
    nationality: str
    language: Language


@dataclass(frozen=True)
class CommunicationStyle:
    brevity: str  # short/medium/long
    formality: str  # casual/polite/professional
    tone: str  # neutral/anxious/friendly/assertive


@dataclass(frozen=True)
class PatientPersona:
    id: str
    demographics: Demographics
    conditions: list[str]
    communication_style: CommunicationStyle


@dataclass(frozen=True)
class ClinicPersona:
    role: str  # receptionist/nurse/doctor
    capabilities: list[str]
    style: dict[str, str]


@dataclass
class Scenario:
    type: str
    goal: str
    constraints: dict[str, Any]
    seed_context: str


@dataclass
class TurnEvent:
    run_id: str
    turn: int
    speaker: Speaker
    text: str
    language: Language
    state: dict[str, Any]
    rewards: dict[str, float]
