from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, List, Set

from ..scenarios.generator import Scenario


@dataclass
class RewardResult:
    success: bool
    total: float
    components: Dict[str, float]


SCENARIO_TERMS: Dict[str, Set[str]] = {
    # English and Arabic key terms
    "appointment_booking": {
        "appointment",
        "book",
        "time",
        "date",
        "slot",
        "location",
        "confirm",
        "موعد",
        "وقت",
        "تاريخ",
        "موقع",
        "تأكيد",
    },
    "follow_up": {
        "follow",
        "follow-up",
        "results",
        "lab",
        "report",
        "schedule",
        "متابعة",
        "نتائج",
        "مختبر",
        "تقرير",
    },
    "emergency": {
        "emergency",
        "urgent",
        "help",
        "pain",
        "bleeding",
        "ambulance",
        "طوارئ",
        "عاجل",
        "مساعدة",
        "ألم",
        "نزيف",
        "إسعاف",
    },
    "complaint": {
        "complaint",
        "issue",
        "billing",
        "refund",
        "escalate",
        "resolve",
        "شكوى",
        "مشكلة",
        "فواتير",
        "استرداد",
        "تصعيد",
        "حل",
    },
}


def _concat_text(turns: Iterable) -> str:
    return " ".join(getattr(t, "text", "") for t in turns).lower()


def _task_completion_score(text: str, scenario_key: str) -> float:
    terms = SCENARIO_TERMS.get(scenario_key, set())
    if not terms:
        return 0.0
    matched = {term for term in terms if term in text}
    return min(1.0, len(matched) / max(3.0, len(terms) / 3.0))


def _satisfaction_score(text: str) -> float:
    positive = any(x in text for x in ["thank you", "thanks", "شكرا", "شكرًا"])  # Arabic variants
    polite = any(x in text for x in ["please", "يرجى"])  # politeness cues
    negative = any(x in text for x in ["not helpful", "bad", "angry", "سيئ", "غاضب"])  # neg cues
    # Base 0.2 to avoid zeroing when neutral; penalize negatives, boost positives
    score = 0.2 + (0.6 if positive else 0.0) + (0.2 if polite else 0.0) - (0.4 if negative else 0.0)
    return max(0.0, min(1.0, score))


def _efficiency_score(num_turns: int) -> float:
    # Ideal <= 6 turns. Degrade linearly to 0 by 20 turns.
    if num_turns <= 6:
        return 1.0
    return max(0.0, 1.0 - (num_turns - 6) / 14.0)


def compute_rewards(turns: List, scenario: Scenario) -> RewardResult:
    text = _concat_text(turns)
    scenario_key = scenario.type.value

    task = _task_completion_score(text, scenario_key)
    satisfaction = _satisfaction_score(text)
    efficiency = _efficiency_score(len(turns))

    # Weighted sum stays within [0, 1]
    total = 0.5 * task + 0.3 * satisfaction + 0.2 * efficiency
    success = (task >= 0.6) and (total >= 0.65)

    components: Dict[str, float] = {
        "task_completion": task,
        "satisfaction": satisfaction,
        "efficiency": efficiency,
    }
    return RewardResult(success=success, total=float(total), components=components)
