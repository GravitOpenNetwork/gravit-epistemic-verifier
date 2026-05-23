from dataclasses import dataclass, asdict
import hashlib
import json
from typing import List, Dict, Any

@dataclass
class EESMetadata:
    verification_id: str
    timestamp: int
    model_id: str
    prompt_hash: str
    intermediate_steps: List[Dict[str, Any]]
    conditions: Dict[str, Any]
    lineage_version: str = "1.0"

    def to_dict(self) -> dict:
        return asdict(self)

    def commitment(self) -> str:
        data = json.dumps(self.to_dict(), sort_keys=True)
        return hashlib.sha256(data.encode('utf-8')).hexdigest()
