import time
from typing import Any, Dict

from deepcore.core import DeepCore, Event
from deepcore.storage.event_store import SQLiteEventStore
from deepcore.streaming.redis_stream import RedisStreamBridge


class EventConsumerWorker:
    """
    Background worker that continuously consumes events from Redis
    and persists them into the ledger + updates system state.
    """

    def __init__(self, redis_client):
        self.store = SQLiteEventStore()
        self.system = DeepCore()
        self.stream = RedisStreamBridge(redis_client)

    def process_event(self, raw: Dict[str, Any]):
        event = Event(**{
            "event_id": raw.get("event_id"),
            "timestamp": raw.get("timestamp"),
            "event_type": raw.get("event_type"),
            "entity": raw.get("entity"),
            "payload": raw.get("payload", {}),
        })

        self.store.append(raw)
        self.system.commit_event(event)

    def run(self):
        last_id = "$"

        while True:
            messages = self.stream.consume(last_id=last_id)

            for stream, events in messages:
                for event_id, data in events:
                    self.process_event(data)
                    last_id = event_id

            time.sleep(1)
