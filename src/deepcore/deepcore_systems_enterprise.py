from deepcore.core import DeepCore, Event
from deepcore.ingestion import StreamingIngestor


def main():
    system = DeepCore()

    # Optional ingestion pipeline (not strictly required for core demo)
    ingestor = StreamingIngestor(system.ledger)

    # Create events via ingestion-style interface
    ingestor.push({
        "event_id": "evt-1",
        "timestamp": "2026-07-06T00:00:00Z",
        "event_type": "ACCOUNT_CREATE",
        "entity": "wallet_1",
        "payload": {"balance": 100}
    })

    ingestor.push({
        "event_id": "evt-2",
        "timestamp": "2026-07-06T00:01:00Z",
        "event_type": "BALANCE_UPDATE",
        "entity": "wallet_1",
        "payload": {"balance": 250}
    })

    # Direct event commit (core path)
    system.commit_event(Event(
        event_id="evt-3",
        timestamp="2026-07-06T00:02:00Z",
        event_type="TRANSFER",
        entity="wallet_1",
        payload={"amount": 50}
    ))

    # Rebuild state
    state = system.get_state()
    state_hash = system.get_state_hash()

    print("STATE:", state)
    print("STATE_HASH:", state_hash)


if __name__ == "__main__":
    main()
