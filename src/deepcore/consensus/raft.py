from enum import Enum
from typing import Dict, List, Optional
import time
import random


class NodeState(str, Enum):
    FOLLOWER = "follower"
    CANDIDATE = "candidate"
    LEADER = "leader"


class RaftNode:
    """
    Minimal Raft-style consensus primitive for DeepCore Systems Enterprise.

    This is NOT production Raft.
    It is a structural consensus skeleton for event ordering across regions.
    """

    def __init__(self, node_id: str, peers: List[str]):
        self.node_id = node_id
        self.peers = peers

        self.state = NodeState.FOLLOWER
        self.current_term = 0
        self.voted_for: Optional[str] = None

        self.log: List[Dict] = []
        self.commit_index = 0

        self.last_heartbeat = time.time()

    def become_leader(self):
        self.state = NodeState.LEADER
        self.voted_for = self.node_id

    def become_candidate(self):
        self.state = NodeState.CANDIDATE
        self.current_term += 1
        self.voted_for = self.node_id

    def become_follower(self, term: int):
        self.state = NodeState.FOLLOWER
        self.current_term = term
        self.voted_for = None

    def append_entry(self, entry: Dict):
        """Append event to local log."""
        self.log.append(entry)

    def replicate_log(self, entry: Dict) -> Dict[str, bool]:
        """
        Simulated replication across peers.
        In real system: RPC + quorum agreement.
        """
        results = {}

        for peer in self.peers:
            # simulate network variability
            success = random.random() > 0.1
            results[peer] = success

        # commit if majority succeed
        success_count = sum(1 for v in results.values() if v)

        if success_count >= (len(self.peers) + 1) // 2:
            self.log.append(entry)
            self.commit_index += 1

        return results

    def get_state(self) -> Dict:
        return {
            "node_id": self.node_id,
            "state": self.state,
            "term": self.current_term,
            "commit_index": self.commit_index,
            "log_length": len(self.log),
        }

    def heartbeat(self):
        self.last_heartbeat = time.time()
