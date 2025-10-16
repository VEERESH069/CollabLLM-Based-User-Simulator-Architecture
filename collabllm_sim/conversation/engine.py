from __future__ import annotations

from dataclasses import dataclass, field

from collabllm_sim.types import Language, Scenario, Speaker, TurnEvent


@dataclass
class ConversationState:
    slots: dict[str, object] = field(default_factory=dict)
    turn_index: int = 0


@dataclass
class RewardWeights:
    alpha: float
    beta: float
    gamma: float
    lambda_: float


class RewardModel:
    def __init__(self, weights: RewardWeights) -> None:
        self.weights = weights

    def score_turn(self, text: str, state: ConversationState) -> dict[str, float]:
        # Placeholder heuristic: longer messages add some progress, encourage mid-length
        length = len(text)
        task_progress = min(1.0, length / 120.0)
        helpfulness = 0.7 if 30 <= length <= 200 else 0.4
        style_alignment = 0.8  # placeholder
        safety_penalty = 0.0
        return {
            "task_progress": task_progress,
            "helpfulness": helpfulness,
            "style_alignment": style_alignment,
            "safety_penalty": safety_penalty,
        }

    def aggregate(self, rewards_over_time: list[dict[str, float]]) -> float:
        total = 0.0
        for r in rewards_over_time:
            total += (
                self.weights.alpha * r.get("task_progress", 0.0)
                + self.weights.beta * r.get("helpfulness", 0.0)
                + self.weights.gamma * r.get("style_alignment", 0.0)
                - self.weights.lambda_ * r.get("safety_penalty", 0.0)
            )
        return total


class ConversationEngine:
    def __init__(
        self,
        scenario: Scenario,
        max_turns: int,
        reward_model: RewardModel,
    ) -> None:
        self.scenario = scenario
        self.max_turns = max_turns
        self.state = ConversationState()
        self.reward_model = reward_model

    async def run(self, run_id: str, language: Language) -> list[TurnEvent]:
        events: list[TurnEvent] = []
        current_speaker = Speaker.PATIENT

        # Seed initial utterance
        patient_text = f"I would like help: {self.scenario.goal}. {self.scenario.seed_context}"
        turn_rewards = self.reward_model.score_turn(patient_text, self.state)
        events.append(
            TurnEvent(
                run_id=run_id,
                turn=self.state.turn_index,
                speaker=current_speaker,
                text=patient_text,
                language=language,
                state=dict(self.state.slots),
                rewards=turn_rewards,
            )
        )
        self.state.turn_index += 1

        # Alternate speakers for a few turns with simple heuristics
        while self.state.turn_index < self.max_turns:
            if current_speaker == Speaker.PATIENT:
                current_speaker = Speaker.CLINIC
                clinic_text = "Let me collect some details to proceed."
                current_progress = self.state.slots.get("progress", 0)
                if not isinstance(current_progress, int):
                    current_progress = 0
                self.state.slots["progress"] = current_progress + 1
                text = clinic_text
            else:
                current_speaker = Speaker.PATIENT
                patient_text = "Here are my details and preferences."
                text = patient_text

            rewards = self.reward_model.score_turn(text, self.state)
            events.append(
                TurnEvent(
                    run_id=run_id,
                    turn=self.state.turn_index,
                    speaker=current_speaker,
                    text=text,
                    language=language,
                    state=dict(self.state.slots),
                    rewards=rewards,
                )
            )
            self.state.turn_index += 1

        return events
