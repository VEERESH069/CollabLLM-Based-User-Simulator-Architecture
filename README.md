 cursor/build-collabllm-user-simulation-for-healthcare-ai-4e5c
# CollabLLM Healthcare Conversation User Simulator

A CollabLLM‑inspired user simulation framework for multi‑turn healthcare conversations. It is designed to test and benchmark Patient AI and Clinic AI services through realistic, bilingual (Arabic/English) conversations that reflect real clinic workflows.

> Status: Early scaffolding. This README documents the target design and how to use it as modules and CLI are added incrementally.

## What this provides
- Patient persona generator (demographics, conditions, communication styles)
- Clinic staff persona simulator (receptionist, nurse, doctor behaviors)
- Multi‑turn conversation engine and state tracking
- Scenario generator (appointment booking, follow‑ups, emergencies, complaints)
- Bilingual simulation for Dubai context (Arabic/English)
- Multi‑turn aware reward/quality metrics (task completion, satisfaction, efficiency)
- Analytics collection and summary reports (+ basic dashboard)
- Automated test pipeline and load testing for concurrent virtual users

Based on principles from CollabLLM (Microsoft Research) on teaching LLMs to collaborate with users.

## Repository layout (planned)
```
collabllm_sim/
  personas/        # patient and clinic personas
  scenarios/       # conversation scenario generation
  conversation/    # state, policy, multi‑turn engine, rewards
  translate/       # Arabic/English translation utilities
  clients/         # thin clients for Patient AI / Clinic AI services
  analytics/       # logging, aggregation, and dashboard data

tests/             # unit, flow, and load tests
```

## Requirements
- Python 3.11+
- Linux/macOS

Optional for later phases:
- `pytest` for tests
- `uvloop`, `httpx`, `pydantic`, `orjson`, `tenacity`, `typer`, `rich` (will be specified in `requirements.txt` / `pyproject.toml` once modules land)

## Setup
1) Create and activate a virtual environment
```bash
python3 -m venv .venv
source .venv/bin/activate
```

2) Install dependencies (when available)
```bash
# Will be added later as code lands
pip install -r requirements.txt
```

## Configuration
Set service endpoints and basic knobs via environment variables or a `.env` file.

- `SIM_PATIENT_SERVICE_URL`: Base URL for Patient AI Service
- `SIM_CLINIC_SERVICE_URL`: Base URL for Clinic AI Service
- `SIM_LANGUAGE`: Default language for simulated users (`en` or `ar`)
- `SIM_OUTPUT_DIR`: Directory to write simulation logs (default: `./outputs`)
- `SIM_RUNS`: Number of conversations to simulate per scenario (e.g., `100`)
- `SIM_CONCURRENCY`: Number of concurrent virtual users (e.g., `50`)
- `SIM_SEED`: Random seed for reproducibility (e.g., `2025`)

Example `.env`:
```ini
SIM_PATIENT_SERVICE_URL=https://patient-ai.example.com
SIM_CLINIC_SERVICE_URL=https://clinic-ai.example.com
SIM_LANGUAGE=en
SIM_OUTPUT_DIR=./outputs
SIM_RUNS=200
SIM_CONCURRENCY=50
SIM_SEED=2025
```

## Quickstart (as components land)
Run a basic simulation once the CLI is added:
```bash
python -m collabllm_sim.cli run \
  --scenario appointment_booking \
  --runs 200 \
  --concurrency 50 \
  --language en \
  --output ./outputs/booking_en
```
Switch to Arabic:
```bash
python -m collabllm_sim.cli run --scenario appointment_booking --language ar
```

Generate a dataset across multiple personas and scenarios:
```bash
python -m collabllm_sim.cli sweep \
  --scenarios appointment_booking,follow_up,emergency,complaint \
  --personas patients:elderly,adult_young,adult_parent \
  --runs 100 --concurrency 30
```

Run built‑in tests:
```bash
pytest -q
```

## Data contracts
### Patient persona (input to simulator)
```json
{
  "id": "patient_12345",
  "demographics": {
    "age": 62,
    "gender": "female",
    "nationality": "UAE",
    "language": "ar"
  },
  "conditions": ["type2_diabetes", "hypertension"],
  "communication_style": {
    "brevity": "short",
    "formality": "polite",
    "tone": "anxious"
  }
}
```

### Clinic persona (role policy)
```json
{
  "role": "receptionist",
  "capabilities": ["book_appointment", "reschedule", "collect_demographics"],
  "style": { "formality": "professional", "tone": "neutral" }
}
```

### Scenario (conversation goal)
```json
{
  "type": "appointment_booking",
  "goal": "book next available cardiology appointment",
  "constraints": { "preferred_window_days": 10, "clinic": "Downtown" },
  "seed_context": "patient has new chest discomfort"
}
```

### Conversation log (JSONL)
Each line is one event.
```json
{
  "run_id": "r_0001",
  "turn": 3,
  "speaker": "patient",  // or "clinic"
  "text": "I'd like to book a cardiology appointment.",
  "language": "en",
  "state": { "slot": "department", "value": "cardiology" },
  "rewards": { "task_progress": 0.4, "helpfulness": 0.7 }
}
```

## Rewards and quality metrics (multi‑turn aware)
At each turn t, compute a shaped reward:

- `task_progress_t`: how much closer we are to scenario goal
- `helpfulness_t`: response quality vs. user needs
- `style_alignment_t`: persona/style adherence
- `safety_penalty_t`: content/safety issues

Aggregate per conversation:

\[ R_total = Σ_t (α·task_progress_t + β·helpfulness_t + γ·style_alignment_t − λ·safety_penalty_t) \]

Report surface metrics:
- **task completion rate**: fraction of conversations that achieved scenario goal
- **satisfaction score**: proxy from helpfulness/style and closing survey intent
- **efficiency**: turns to completion; median/percentiles
- **handoff/abandon rate**: where goal was not achieved

## Bilingual simulation (Arabic/English)
- Personas specify `language` (`en`/`ar`)
- Requests/responses are translated as needed so services can be evaluated in both languages
- Evaluation and analytics use a canonical form to ensure fair scoring across languages

## Integrations (service clients)
Minimal HTTP clients will be provided for:
- `Patient AI Service (Testing)` — mockable endpoints for patient‑side interactions
- `Clinic AI Service (Testing)` — receptionist/nurse/doctor behaviors

Set `SIM_PATIENT_SERVICE_URL` and `SIM_CLINIC_SERVICE_URL` to point to your test deployments.

## Analytics and dashboard
- Raw logs: JSONL per run under `SIM_OUTPUT_DIR`
- Aggregates: `summary.json` and `summary.csv`
- Basic static dashboard will read aggregates and visualize:
  - success rates by scenario/persona/language
  - failure patterns and common breakdowns
  - conversation length distributions

## Testing
Planned tests (to be added under `tests/`):
- Unit: persona variety/consistency; scenario creation; bilingual accuracy; state management
- Flow: end‑to‑end journeys (booking→completion) across scenarios
- Load: hundreds of concurrent virtual users and long runs

Run tests:
```bash
pytest -q
```

## Roadmap (estimated)
- Dev (≈9 days)
  - Personas, scenarios, conversation engine, bilingual, rewards, clients, analytics, CLI, dashboard
- Tests (≈3 days)
  - Unit tests, flow tests, load tests

## Contributing
- Use feature branches and small PRs
- Add/extend tests for new behaviors
- Keep personas/scenarios realistic and privacy‑safe

## License
TBD
=======
# Collab Sim

CollabLLM-inspired simulation framework for multi-turn healthcare conversations.

## Quick start

- Install: `pip install -e .[test]`
- Run CLI: `collab-sim run --scenario appointment_booking --language bilingual --num-conversations 3`
- Show personas: `collab-sim personas -n 5`
- Dashboard: `pip install -e .[dashboard] && collab-sim dashboard`

## Structure

- `src/collab_sim/personas`: patient and clinic personas
- `src/collab_sim/scenarios`: scenario generator
- `src/collab_sim/lang`: bilingual helpers (en/ar)
- `src/collab_sim/connectors`: connectors to Patient AI and Clinic AI (stubs)
- `src/collab_sim/env`: multi-turn conversation simulator
- `src/collab_sim/rewards`: reward/metrics
- `src/collab_sim/analytics`: logging and dashboard
- `tests`: unit, flow, load

## Notes

This initial version uses stubbed clients. Replace with real HTTP clients to integrate with Patient AI Service and Clinic AI Service.

