from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional

import requests


@dataclass
class HttpAIServiceClient:
    base_url: str
    api_key: Optional[str] = None
    timeout_s: float = 15.0

    def _headers(self) -> Dict[str, str]:
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        return headers

    def respond(self, message: str, *, language: str = "en") -> str:
        payload = {"message": message, "language": language}
        url = f"{self.base_url.rstrip('/')}/respond"
        resp = requests.post(url, json=payload, headers=self._headers(), timeout=self.timeout_s)
        resp.raise_for_status()
        data = resp.json()
        return str(data.get("text", ""))
