from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd
import streamlit as st


parser = argparse.ArgumentParser()
parser.add_argument("--log-path", type=Path, default=Path("sim_runs/sim_log.jsonl"))


def main() -> None:
    args = parser.parse_args()
    st.set_page_config(page_title="Collab Sim Dashboard", layout="wide")
    st.title("Simulation Analytics")

    if not args.log_path.exists():
        st.warning(f"No log found at {args.log_path}")
        return

    records = []
    with args.log_path.open("r", encoding="utf-8") as f:
        for line in f:
            records.append(json.loads(line))

    df = pd.DataFrame(records)

    summaries = df[df["type"] == "summary"]
    turns = df[df["type"] == "turn"]

    st.subheader("Overview")
    col1, col2, col3 = st.columns(3)
    col1.metric("Conversations", len(summaries))
    col2.metric("Success Rate", f"{summaries['success'].mean():.2%}" if len(summaries) else "0%")
    col3.metric("Avg Reward", f"{summaries['total_reward'].mean():.3f}" if len(summaries) else "0.000")

    st.subheader("By Scenario")
    if len(summaries):
        st.dataframe(
            summaries.groupby("scenario").agg(
                count=("scenario", "count"),
                success_rate=("success", "mean"),
                avg_reward=("total_reward", "mean"),
            )
        )

    st.subheader("Sample Turns")
    st.dataframe(turns.tail(50))


if __name__ == "__main__":  # pragma: no cover
    main()
