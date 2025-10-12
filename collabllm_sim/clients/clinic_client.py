from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class ClinicClient:
    base_url: str | None

    async def respond(self, message: str, context: dict[str, Any] | None = None) -> str:
        # Stub: echo for now; replace with real service calls
        return f"CLINIC_AI_ECHO: {message}"
