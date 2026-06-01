"""
History Keeper — persistent storage of epistemic proofs.
"""

import json
from typing import Dict, Any, List, Optional


class HistoryKeeper:
    def __init__(self, storage_path: str = "proofs.json"):
        self.storage_path = storage_path
        self.proofs = []
        self._load()

    def store(self, proof: Dict[str, Any]) -> str:
        proof_id = proof.get("trace_id", f"proof_{len(self.proofs)}")
        self.proofs.append({"id": proof_id, "data": proof, "timestamp": proof.get("timestamp")})
        self._save()
        return proof_id

    def get(self, proof_id: str) -> Optional[Dict[str, Any]]:
        for p in self.proofs:
            if p["id"] == proof_id:
                return p["data"]
        return None

    def list(self, limit: int = 100) -> List[Dict[str, Any]]:
        return self.proofs[-limit:]

    def _load(self):
        try:
            with open(self.storage_path, "r") as f:
                self.proofs = json.load(f)
        except FileNotFoundError:
            self.proofs = []

    def _save(self):
        with open(self.storage_path, "w") as f:
            json.dump(self.proofs, f, indent=2)
