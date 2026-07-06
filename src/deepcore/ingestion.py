from dataclasses import dataclass
from typing import Dict, Any, Optional
import time
import uuid


@dataclass
class IngestedEvent:
    event_id: str
    timestamp: str
    event_type: str
    entity: str
    payload: Dict[str, Any]
    source: str = "ingestion"


class EventIngestionPipeline:
    """
    Validates and normalizes incoming events before entering the ledger.
    """

    def validate(self, event: IngestedEvent) -> bool:
        if not event.event_id or not event.entity:
            return False
        if not isinstance(event.payload, dict):
            return False
        return True

    def normalize(self, raw: Dict[str, Any]) -> IngestedEvent:
        return IngestedEvent(
            event_id=raw.get("event_id", str(uuid.uuid4())),
            timestamp=raw.get("timestamp", str(time.time())),
            event_type=raw.get("event_type", "UNKNOWN"),
            entity=raw.get("entity", "unknown"),
            payload=raw.get("payload", {}),
        )


class Ingestor:
    def __init__(self, ledger):
        self.ledger = ledger
        self.pipeline = EventIngestionPipeline()

    def ingest(self, raw_event: Dict[str, Any]) -> Optional[str]:
        event = self.pipeline.normalize(raw_event)

        if not self.pipeline.validate(event):
            return None

        self.ledger.append(event)
        return event.event_id


class StreamingIngestor:
    """Lightweight streaming ingestion interface."""

    def __init__(self, ledger):
        self.ingestor = Ingestor(ledger)

    def push(self, event: Dict[str, Any]) -> str:
        return self.ingestor.ingest(event)
