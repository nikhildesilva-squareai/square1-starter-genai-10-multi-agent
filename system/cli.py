"""CLI:  python -m system.cli "Implement a function that parses an ISO timestamp"

Loads the agent roster and the offline mock LLM fixture so you can run the whole
crew without a network or an API key (the default). Pass --live to use the real
Anthropic model behind run_agent once you've wired it up.
"""
import argparse
import json
import os

from .orchestrator import orchestrate

DATASET_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "dataset")
SPECS_PATH = os.path.join(DATASET_DIR, "agent_specs.json")
MOCK_PATH = os.path.join(DATASET_DIR, "mock_llm.json")


def load_agents() -> list[dict]:
    with open(SPECS_PATH, encoding="utf-8") as f:
        return json.load(f)


def make_mock():
    """Return a mock(agent_name) -> completion backed by the offline fixture."""
    with open(MOCK_PATH, encoding="utf-8") as f:
        index = json.load(f)

    def mock(agent_name: str) -> str:
        return index.get(agent_name, f"[no mock completion for {agent_name}]")

    return mock


def main() -> None:
    ap = argparse.ArgumentParser(description="Multi-Agent AI System — route, run, aggregate.")
    ap.add_argument("task", help="The task to hand to the agent crew.")
    ap.add_argument("--live", action="store_true",
                    help="Use the real Anthropic model instead of the offline mock.")
    args = ap.parse_args()

    agents = load_agents()
    mock = None if args.live else make_mock()

    result = orchestrate(args.task, agents, mock=mock)

    print("=== Final deliverable ===")
    print(result["final"])
    print("\n=== Transcript (in order) ===")
    for msg in result["transcript"]:
        print(f"[{msg['sender']}] {msg['content']}")


if __name__ == "__main__":
    main()
