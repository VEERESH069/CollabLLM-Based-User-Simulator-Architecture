from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.table import Table

from .personas.patient import PatientPersona, generate_patient_persona
from .personas.clinic import ClinicPersona, generate_clinic_persona
from .scenarios.generator import Scenario, ScenarioType, generate_scenario
from .env.simulator import ConversationSimulator
from .connectors.stub_client import StubAIServiceClient
from .analytics.logger import SimulationLogger
from .analytics.summary import summarize_log

app = typer.Typer(add_completion=False, help="Run healthcare conversation simulations.")
console = Console()


@app.command()
def personas(
    n: int = typer.Option(3, help="Number of personas to generate"),
    language: str = typer.Option("en", help="Primary language: en|ar|bilingual"),
    seed: Optional[int] = typer.Option(None, help="Random seed"),
):
    rows = []
    for i in range(n):
        rows.append(generate_patient_persona(primary_language=language, seed=(seed or 0) + i))
    table = Table(title="Sample Patient Personas")
    table.add_column("Name")
    table.add_column("Age")
    table.add_column("Gender")
    table.add_column("Language")
    table.add_column("Conditions")
    for p in rows:
        table.add_row(p.name, str(p.age), p.gender, p.primary_language, ", ".join(p.conditions))
    console.print(table)


@app.command()
def run(
    scenario: ScenarioType = typer.Option(
        ScenarioType.appointment_booking, case_sensitive=False, help="Scenario type"
    ),
    language: str = typer.Option("en", help="Conversation language: en|ar|bilingual"),
    max_turns: int = typer.Option(10, help="Maximum number of turns"),
    num_conversations: int = typer.Option(1, help="How many parallel conversations to run"),
    log_path: Optional[Path] = typer.Option(None, help="Path to write JSONL logs"),
    seed: Optional[int] = typer.Option(None, help="Random seed for reproducibility"),
):
    log_path = log_path or Path("sim_runs/sim_log.jsonl")
    log_path.parent.mkdir(parents=True, exist_ok=True)
    logger = SimulationLogger(log_path)

    for i in range(num_conversations):
        patient = generate_patient_persona(primary_language=language, seed=(seed or 0) + i)
        clinic = generate_clinic_persona(seed=(seed or 0) + 1000 + i)
        scen = generate_scenario(scenario_type=scenario)

        patient_client = StubAIServiceClient(role="patient")
        clinic_client = StubAIServiceClient(role="clinic", scenario=scen)

        sim = ConversationSimulator(
            patient=patient,
            clinic=clinic,
            scenario=scen,
            patient_client=patient_client,
            clinic_client=clinic_client,
            logger=logger,
        )
        result = sim.run(max_turns=max_turns)
        console.print(
            f"[bold]Conversation {i+1}[/bold]: success={result.success} turns={result.turns} reward={result.total_reward:.3f}"
        )

    summary = summarize_log(log_path)
    console.print("\n[bold]Summary[/bold]")
    console.print(json.dumps(summary, indent=2))


@app.command()
def dashboard(log_path: Path = typer.Argument(Path("sim_runs/sim_log.jsonl"))):
    """Launch a simple dashboard to explore results (requires extra 'dashboard' deps)."""
    try:
        import streamlit.web.cli as stcli  # type: ignore
    except Exception as exc:  # pragma: no cover
        console.print("Install optional deps: pip install -e .[dashboard]")
        raise typer.Exit(code=1) from exc

    script = Path(__file__).with_name("../analytics/dashboard.py").resolve()
    stcli.main(["streamlit", "run", str(script), "--", "--log-path", str(log_path)])


def main() -> None:
    app()
