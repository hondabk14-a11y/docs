from fastapi import FastAPI
from typing import Dict, Any

from deepcore.core import DeepCore, Event
from deepcore.storage.event_store import SQLiteEventStore

app = FastAPI(title="DeepCore Systems Enterprise API")

store = SQLiteEventStore()
system = DeepCore()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/events")
def add_event(event: Dict[str, Any]):
    store.append(event)
    system.commit_event(Event(**event))
    return {"status": "accepted", "event_id": event.get("event_id")}

@app.get("/state")
def get_state():
    return system.get_state()

@app.get("/state/hash")
def get_state_hash():
    return {"hash": system.get_state_hash()}

@app.post("/replay")
def replay():
    return system.get_state()