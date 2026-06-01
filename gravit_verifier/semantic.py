"""
Semantic verifier for intent/action alignment.
"""

from __future__ import annotations

import re
from typing import Dict


class SemanticVerifier:
    def score(self, intent_text: str, action_text: str) -> Dict[str, float]:
        intent_tokens = self._tokens(intent_text)
        action_tokens = self._tokens(action_text)
        if not intent_tokens or not action_tokens:
            score = 0.0
        else:
            overlap = len(intent_tokens & action_tokens) / max(len(intent_tokens), 1)
            aligned_tokens = {"transfer", "send", "pay", "invoice", "iban", "verified", "supplier", "eurau"}
            boost = 0.1 * len((intent_tokens | action_tokens) & aligned_tokens)
            penalties = 0.0
            if {"unknown", "wallet", "deadbeef", "bypass"} & action_tokens:
                penalties += 0.3
            if {"ignore", "reject", "unauthorized"} & intent_tokens:
                penalties += 0.15
            score = min(0.99, max(0.0, 0.28 + 0.42 * overlap + boost - penalties))
        return {"semantic_score": float(score)}

    def _tokens(self, text: str) -> set[str]:
        return {token for token in re.findall(r"[a-z0-9]+", (text or "").lower()) if token}
