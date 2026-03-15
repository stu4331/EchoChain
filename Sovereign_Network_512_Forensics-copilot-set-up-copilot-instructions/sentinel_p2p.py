"""
Sentinel P2P Mesh Network
- Peer discovery
- Expression synchronization
- Local/network toggle

Lightweight stub for the decentralized vision.
"""

from dataclasses import dataclass
from typing import List, Dict, Optional
import time
import socket


@dataclass
class PeerInfo:
    host: str
    port: int
    last_seen: float
    node_id: str


class SentinelP2P:
    def __init__(self, listen_host: str = "0.0.0.0", listen_port: int = 40833):
        self.listen_host = listen_host
        self.listen_port = listen_port
        self.peers: Dict[str, PeerInfo] = {}
        self.running = False

    def start_node(self):
        """Start listening for peers (stub)."""
        self.running = True
        # Placeholder: actual socket server would start here
        return True

    def stop_node(self):
        """Stop the node."""
        self.running = False

    def register_peer(self, host: str, port: int, node_id: str):
        self.peers[node_id] = PeerInfo(host=host, port=port, last_seen=time.time(), node_id=node_id)

    def discover_peers(self) -> List[PeerInfo]:
        """Return currently known peers."""
        return list(self.peers.values())

    def broadcast_expression(self, expression_payload: dict) -> int:
        """Broadcast an expression to all peers (stub)."""
        # In real implementation: send over sockets with retry/backoff
        return len(self.peers)

    def get_status(self) -> dict:
        return {
            "running": self.running,
            "peer_count": len(self.peers),
            "listen_host": self.listen_host,
            "listen_port": self.listen_port,
        }
