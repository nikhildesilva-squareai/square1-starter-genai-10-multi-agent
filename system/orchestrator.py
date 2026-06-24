"""
Multi-Agent AI System — orchestrator core.

A crew of specialised agents (researcher, coder, writer, critic) coordinated by
an orchestrator over a shared message bus. The four functions below are the
contract:

  route(task, agents)   -> pick the single agent that should handle a task
  run_agent(agent, task) -> run one agent (Anthropic SDK live; mock offline)
  aggregate(results)    -> merge several agents' outputs into one deliverable
  orchestrate(task)     -> the full loop, recording every step on a MessageBus

The three tests in tests/ define the contract for route(), aggregate(), and the
message bus. Implement the stubs until they pass, then wire run_agent() to the
real Anthropic tool-use loop.

Models (current ids only — NEVER claude-3-*):
  - default: claude-sonnet-4-6
  - cheap:   claude-haiku-4-5-20251001   (the agent with cheap=True)
Read the key from the ANTHROPIC_API_KEY environment variable only.
"""
from __future__ import annotations
from typing import Any, Callable

from .bus import MessageBus


def route(task: str, agents: list[dict]) -> dict:
    """Pick the single agent that should handle `task`.

    `agents` is the list of agent specs (see dataset/agent_specs.json): each has
    a `name` and a list of lowercased `triggers`.

    TODO:
      - return the agent whose `triggers` match the task text (case-insensitive).
      - if NO agent matches, raise ValueError(f"No agent can handle task: {task!r}")
        (an unroutable task is an error — the tests require this).
    The sample material guarantees exactly one agent matches each scenario, so a
    simple trigger match recovers the labelled agent for all of them.
    """
    raise NotImplementedError("Implement route")


def run_agent(
    agent: dict,
    task: str,
    mock: Callable[[str], str] | None = None,
) -> str:
    """Run one agent on a task and return its output text.

    `mock` is the swappable model backend: a function name -> completion. In
    tests and `--mock` runs it is the offline fixture (mock_llm.json), so no
    network or API key is needed; in production it is None and you call the real
    model.

    TODO:
      - if `mock` is not None: return mock(agent["name"]).
      - otherwise: call the Anthropic SDK with the agent's `system` prompt and
        `model` (claude-sonnet-4-6 by default, claude-haiku-4-5-20251001 when
        agent["cheap"] is True), passing `task` as the user message, and return
        the text of the response. Read the key from ANTHROPIC_API_KEY. If the
        agent exposes tools, drive the tool_use -> tool_result loop properly.
    """
    raise NotImplementedError("Implement run_agent")


def aggregate(results: list[dict]) -> str:
    """Merge several agents' outputs into one coherent, attributed deliverable.

    `results` is a list of dicts like {"agent": <name>, "output": <text>}.

    TODO: return a single string that combines every result and attributes each
    section to the agent that produced it (e.g. a labelled section per agent).
    Preserve the order of `results`. Do not drop any agent's output.
    """
    raise NotImplementedError("Implement aggregate")


def orchestrate(
    task: str,
    agents: list[dict],
    mock: Callable[[str], str] | None = None,
) -> dict:
    """The full multi-agent loop.

    TODO:
      1. create a MessageBus and append the incoming task.
      2. route(task, agents) -> chosen agent; append the routing decision.
      3. run_agent(chosen, task, mock) -> output; append it.
      4. (optional, recommended) hand the output to the critic agent for review
         and append that too.
      5. aggregate the results into the final deliverable; append it.
    Return {"final": <aggregated str>, "transcript": bus.read()} so the caller
    gets both the deliverable and the ordered record of how it was produced.
    """
    raise NotImplementedError("Implement orchestrate")
