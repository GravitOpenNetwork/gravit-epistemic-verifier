import hashlib
import json
from dataclasses import dataclass


@dataclass
class EESMetadata:
    origin: str
    prompt_hash: str
    model_id: str
    timestamp: int
    intermediate_steps: list[dict]
    conditions: dict

    def commitment(self) -> str:
        data = json.dumps(self.__dict__, sort_keys=True)
        return hashlib.sha256(data.encode()).hexdigest()
