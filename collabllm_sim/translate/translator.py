from __future__ import annotations

from collabllm_sim.types import Language


class Translator:
    def __init__(self) -> None:
        # Placeholder for future integration (e.g., fastText, cloud translate)
        self._noop = True

    def translate(self, text: str, source: Language, target: Language) -> str:
        if source == target:
            return text
        # Minimal stub: tag translations to make tests deterministic without external APIs
        direction = f"{source.value}->{target.value}"
        return f"[{direction}] {text}"
