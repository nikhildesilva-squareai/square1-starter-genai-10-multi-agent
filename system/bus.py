"""
Shared message bus for the agent crew.

Every step the orchestrator takes (a routing decision, an agent result, a
hand-off to the critic) is appended here, and `read()` returns the messages in
the exact order they were appended (FIFO). That ordered transcript is what makes
a multi-agent run auditable.

The starter is an in-memory list — enough to pass the contract test. For the
stretch goal, back it with Redis or Supabase (same append/read contract) so
agents can run as separate workers and the conversation survives a restart.

Tests define the contract for append -> read ordering.
"""
from __future__ import annotations
from typing import Any


class MessageBus:
    """An ordered append-only log of agent messages."""

    def __init__(self) -> None:
        # TODO: initialise whatever storage backs the bus (a list is fine to start).
        raise NotImplementedError("Implement MessageBus.__init__")

    def append(self, sender: str, content: Any) -> None:
        """Append a message from `sender` with `content` to the end of the log."""
        raise NotImplementedError("Implement MessageBus.append")

    def read(self) -> list[dict]:
        """Return all messages in append order (FIFO).

        Each message is a dict like {"sender": <str>, "content": <Any>}.
        The order of this list MUST match the order append() was called.
        """
        raise NotImplementedError("Implement MessageBus.read")
