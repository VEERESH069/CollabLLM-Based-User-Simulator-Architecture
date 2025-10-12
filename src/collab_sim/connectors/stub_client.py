from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from ..lang.bilingual import to_language
from ..scenarios.generator import Scenario


@dataclass
class StubAIServiceClient:
    role: str
    scenario: Optional[Scenario] = None

    def respond(self, message: str, *, language: str = "en") -> str:
        if self.role == "patient":
            return to_language("I need help", "أحتاج مساعدة", language)
        if self.role == "clinic":
            if self.scenario and self.scenario.type.value == "appointment_booking":
                return to_language("Please share your preferred time.", "يرجى مشاركة الوقت المفضل.", language)
            return to_language("How can I assist?", "كيف أستطيع المساعدة؟", language)
        return to_language("Okay", "حسنًا", language)
