from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict


def summarize_log(path: Path) -> Dict[str, Any]:
    totals = defaultdict(lambda: {
        "count": 0,
        "success": 0,
        "reward_sum": 0.0,
        "components_sum": defaultdict(float),
    })
    try:
        with path.open("r", encoding="utf-8") as f:
            for line in f:
                rec = json.loads(line)
                if rec.get("type") == "summary":
                    key = rec.get("scenario", "unknown")
                    totals[key]["count"] += 1
                    totals[key]["success"] += 1 if rec.get("success") else 0
                    totals[key]["reward_sum"] += float(rec.get("total_reward", 0.0))
                    comps = rec.get("components", {}) or {}
                    for k, v in comps.items():
                        totals[key]["components_sum"][k] += float(v)
    except FileNotFoundError:
        return {"scenarios": {}, "overall_success_rate": 0.0}

    scenarios: Dict[str, Any] = {}
    total_count = 0
    total_success = 0
    overall_components_sum: Dict[str, float] = defaultdict(float)
    for k, v in totals.items():
        count = v["count"]
        success = v["success"]
        reward_sum = v["reward_sum"]
        comps_sum = v["components_sum"]
        comps_avg = {ck: (cv / count) if count else 0.0 for ck, cv in comps_sum.items()}
        scenarios[k] = {
            "count": count,
            "success_rate": (success / count) if count else 0.0,
            "avg_reward": (reward_sum / count) if count else 0.0,
            "components_avg": comps_avg,
        }
        total_count += count
        total_success += success
        for ck, cv in comps_sum.items():
            overall_components_sum[ck] += cv

    overall = (total_success / total_count) if total_count else 0.0
    overall_components_avg = {
        ck: (cv / total_count) if total_count else 0.0 for ck, cv in overall_components_sum.items()
    }
    return {
        "scenarios": scenarios,
        "overall_success_rate": overall,
        "overall_components_avg": overall_components_avg,
    }
