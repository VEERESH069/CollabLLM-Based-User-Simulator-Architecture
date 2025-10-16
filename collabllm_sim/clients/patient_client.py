from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class PatientClient:
    base_url: str | None

    async def respond(self, message: str, context: dict[str, Any] | None = None) -> str:
        # Stub: echo for now; replace with real service calls
        return f"PATIENT_AI_ECHO: {message}"
