# Sample material — Multi-Agent AI System

**Sample material — Square 1-owned (synthetic), free for learners.** Three small JSON files, not a CSV. Together they let the full *route → run → aggregate → orchestrate* multi-agent loop run **offline** (no network, no API key) so your contract tests are deterministic.

> ⚠️ Every task, agent, and canned completion below is **invented**. The point is a controlled mini-world where the *right* agent for each task is knowable, so a correct router (and a correct orchestration loop) is gradeable without calling a live model.

Regenerate any time with `python generate_dataset.py` (seed 42).

## `agent_specs.json`
The roster of specialised agents the orchestrator coordinates. One object per agent.

| Field | Type | Description |
|---|---|---|
| `name` | string | Agent id, e.g. `coder`. Routing and the mock LLM key on this. |
| `role` | string | One-line description of what the agent does. |
| `system` | string | The system prompt that defines the agent's behaviour (used when you call the real model). |
| `triggers` | string[] | Lowercased keywords a correct router matches against the task text to pick this agent. |
| `model` | string | Which model the agent uses — `claude-sonnet-4-6` (default) or `claude-haiku-4-5-20251001` (cheap). Never `claude-3-*`. |
| `cheap` | bool | True for the Haiku-backed agent; a cost-aware orchestrator can route cheap work here. |

## `task_scenarios.json`
The orchestrator's inputs — ~8 incoming tasks, each labelled with the agent that should handle it.

| Field | Type | Description |
|---|---|---|
| `id` | string | Scenario id, e.g. `s04`. |
| `task` | string | A natural-language task. Contains a trigger for **exactly one** agent. |
| `expected_agent` | string | The agent `name` a correct router must return for this task (the routing ground truth). |

Scenario order is shuffled, so you can't rely on position — route on the text.

## `mock_llm.json`
A deterministic stand-in for the Anthropic API. A JSON object keyed by **agent name**; each value is the canned completion that agent returns for its task.

| Key | Type | Description |
|---|---|---|
| `<agent name>` | string | The text the agent "produces" offline. In tests, `run_agent` returns this instead of calling the model; in production `run_agent` calls Claude with the agent's `system` prompt + the task. |

**What to build with it:** read the task → `route` it to the right agent by matching the agent `triggers` → `run_agent` the chosen agent (mock offline, real model live) → `aggregate` results from multiple agents into one merged output → wrap it all in an `orchestrate` loop with a shared, ordered message bus. The baked-in signal: every scenario's task matches exactly one agent's triggers and no other's, so a correct router recovers `expected_agent` for all 8 scenarios — an incorrect one is measurably wrong.

_Licence: Sample material — Square 1-owned (synthetic). No attribution required. Regenerate with `generate_dataset.py` (seed 42)._
