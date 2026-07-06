import sqlite3
from typing import Dict, Any, List, Optional
import json


class SQLiteEventStore:
    """
    Persistent append-only event store for DeepCore Systems Enterprise.
    """

    def __init__(self, db_path: str = "deepcore.db"):
        self.conn = sqlite3.connect(db_path)
        self._init_schema()

    def _init_schema(self):
        cursor = self.conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS events (
                event_id TEXT PRIMARY KEY,
                timestamp TEXT,
                event_type TEXT,
                entity TEXT,
                payload TEXT,
                source TEXT
            )
            """
        )
        self.conn.commit()

    def append(self, event: Dict[str, Any]):
        cursor = self.conn.cursor()
        cursor.execute(
            """
            INSERT OR REPLACE INTO events
            (event_id, timestamp, event_type, entity, payload, source)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                event["event_id"],
                event["timestamp"],
                event["event_type"],
                event["entity"],
                json.dumps(event.get("payload", {})),
                event.get("source", "ingestion"),
            ),
        )
        self.conn.commit()

    def get_all(self) -> List[Dict[str, Any]]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM events ORDER BY timestamp ASC")
        rows = cursor.fetchall()

        return [
            {
                "event_id": r[0],
                "timestamp": r[1],
                "event_type": r[2],
                "entity": r[3],
                "payload": json.loads(r[4]),
                "source": r[5],
            }
            for r in rows
        ]
