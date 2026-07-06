from typing import Dict, Any
import json


class RedisStreamBridge:
    """
    Streaming layer for DeepCore Systems Enterprise using Redis Streams.
    Enables event propagation beyond request/response API calls.
    """

    def __init__(self, redis_client, stream_name: str = "deepcore-events"):
        self.redis = redis_client
        self.stream_name = stream_name

    def publish(self, event: Dict[str, Any]) -> str:
        payload = {
            "event_id": event.get("event_id"),
            "timestamp": event.get("timestamp"),
            "event_type": event.get("event_type"),
            "entity": event.get("entity"),
            "payload": json.dumps(event.get("payload", {})),
        }

        return self.redis.xadd(self.stream_name, payload)

    def consume(self, last_id: str = "$", count: int = 10):
        return self.redis.xread({self.stream_name: last_id}, count=count)
