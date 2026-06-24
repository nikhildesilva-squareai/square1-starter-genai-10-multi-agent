"""Contract tests — fail against the starter stubs; make them pass.

All three run OFFLINE: no network, no API key. They use tiny in-test data (not
the dataset fixture) and never call the real model — they pin the deterministic
routing, aggregation, and message-ordering logic, which is the heart of the
orchestrator.
"""
import pytest

from system import route, aggregate, MessageBus


# A tiny in-test agent roster (NOT the big dataset fixture).
AGENTS = [
    {"name": "coder", "triggers": ["implement", "code", "function"]},
    {"name": "writer", "triggers": ["write", "draft", "summarise"]},
    {"name": "critic", "triggers": ["review", "check", "assess"]},
]


def test_route_picks_correct_agent_and_raises_on_unknown():
    # The task matches exactly one agent's triggers -> that agent is chosen.
    chosen = route("Implement a function to parse a date", AGENTS)
    assert chosen["name"] == "coder"

    chosen = route("Please review this pull request", AGENTS)
    assert chosen["name"] == "critic"

    # A task no agent can handle is an error.
    with pytest.raises(ValueError):
        route("Order a pizza for the team", AGENTS)


def test_aggregate_merges_multiple_agent_results():
    results = [
        {"agent": "researcher", "output": "Found three pricing models."},
        {"agent": "writer", "output": "Here is the summary."},
    ]
    merged = aggregate(results)
    assert isinstance(merged, str) and merged.strip()
    # Every agent's output must survive the merge.
    assert "Found three pricing models." in merged
    assert "Here is the summary." in merged


def test_message_bus_preserves_append_order():
    bus = MessageBus()
    bus.append("orchestrator", "task received")
    bus.append("coder", "wrote the function")
    bus.append("critic", "looks good")

    msgs = bus.read()
    assert [m["sender"] for m in msgs] == ["orchestrator", "coder", "critic"]
    assert [m["content"] for m in msgs] == [
        "task received",
        "wrote the function",
        "looks good",
    ]
