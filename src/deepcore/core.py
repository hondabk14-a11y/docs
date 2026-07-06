from dataclasses import dataclass, field
from typing import Any, Dict, List
import hashlib
import json


# -----------------------------
# Event Model
# -----------------------------
@dataclass
class Event:
    event_id: str
    timestamp: str
    event_type: str
    entity: str
    payload: Dict[str, Any]
    metadata: Dict[str, Any] = field(default_factory=dict)


# -----------------------------
# Event Ledger
# -----------------------------
class EventLedger:
    def __init__(self):
        self.events: List[Event] = []

    def append(self, event: Event):
        self.events.append(event)

    def get_all(self) -> List[Event]:
        return self.events


# -----------------------------
# State Engine
# -----------------------------
class StateEngine:
    def __init__(self):
        self.state: Dict[str, Any] = {}

    def apply(self, state: Dict[str, Any], event: Event) -> Dict[str, Any]:
        if event.entity not in state:
            state[event.entity] = {}

        state[event.entity][event.event_type] = event.payload
        return state


# -----------------------------
# Replay Engine
# -----------------------------
class ReplayEngine:
    def __init__(self, ledger: EventLedger, engine: StateEngine):
        self.ledger = ledger
        self.engine = engine

    def replay(self) -> Dict[str, Any]:
        state: Dict[str, Any] = {}
        for event in self.ledger.get_all():
            state = self.engine.apply(state, event)
        return state


# -----------------------------
# Cryptographic Anchoring
# -----------------------------
class CryptoAnchor:
    @staticmethod
    def hash_state(state: Dict[str, Any]) -> str:
        encoded = json.dumps(state, sort_keys=True).encode()
        return hashlib.sha256(encoded).hexdigest()


# -----------------------------
# DeepCore Runtime
# -----------------------------
class DeepCore:
    def __init__(self):
        self.ledger = EventLedger()
        self.engine = StateEngine()
        self.replay = ReplayEngine(self.ledger, self.engine)

    def commit_event(self, event: Event):
        self.ledger.append(event)

    def get_state(self) -> Dict[str, Any]:
        return self.replay.replay()

    def get_state_hash(self) -> str:
        state = self.get_state()
        return CryptoAnchor.hash_state(state)
