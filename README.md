# Multi-Agent AI System — Square 1 AI starter

**Part of [Square 1 AI](https://square1-tutor.vercel.app) · Generative AI · Project 10.**

✅ **Data included.** The dataset is committed in [`dataset/`](dataset/) and is the **same standardized dataset every learner uses** — so results are comparable. It is 100% synthetic and Square 1-owned (no third-party or personal data). You can also download it as a single file from the project page on Square 1.

To run the commands below, copy the files into `data/` (`mkdir -p data && cp -r dataset/* data/`) or point the commands straight at `dataset/`.

MIT licensed — fork it, build on it, put it in your portfolio.

---

# Multi-Agent AI System — starter

Starter for Square 1 AI **Generative AI · Project 10 (Capstone)**. Build a crew of specialised agents — researcher, coder, writer, critic — coordinated by an orchestrator over a shared message bus.

## Setup
```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Get the sample material
The `dataset/` folder (one level up from this starter, on your project page → Resources) holds the agent specs, ~8 task scenarios, and the offline mock LLM fixture. The CLI loads them automatically — no API key needed for the offline path.

## Your task
Three tests define the contract — they fail until you implement the stubs in `system/orchestrator.py` and `system/bus.py`:
```bash
pytest -q
python -m system.cli "Implement a function that parses an ISO-8601 timestamp"
```
Pipeline: `route(task, agents)` → `run_agent(agent, task)` → `aggregate(results)`, all wrapped in `orchestrate(task)` which records every step on a `MessageBus`. The three tests pin the deterministic parts (routing picks the right agent and raises on an unknown task, aggregation merges multiple results, the bus preserves append→read order); they run **offline** with no API key.

Then wire `run_agent` to the real **Anthropic SDK**: read the key from `ANTHROPIC_API_KEY`, give each agent its own system prompt, and use current model ids — `claude-sonnet-4-6` (default) and `claude-haiku-4-5-20251001` (the cheap agent). **Never** `claude-3-*`. If an agent uses tools, drive the `tool_use` → `tool_result` loop properly.

Full brief, rubric, and references are on your Square 1 project page. MIT licensed.
