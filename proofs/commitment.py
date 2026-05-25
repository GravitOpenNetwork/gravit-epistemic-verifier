import hashlib
import json

from gravit_verifier.ees.metadata import EESMetadata


def build_proof(intent: str, action: str, ees: EESMetadata, verdict: str):
    data = {
        "intent_hash": hashlib.sha256(intent.encode()).hexdigest(),
        "action_hash": hashlib.sha256(action.encode()).hexdigest(),
        "ees_commitment": ees.commitment(),
        "verdict": verdict,
    }
    proof_data = json.dumps(data, sort_keys=True)
    signature = hashlib.sha256(proof_data.encode()).hexdigest()
    return {"signature": signature, "proof_data": data}
