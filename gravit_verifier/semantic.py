import numpy as np
from typing import List, Dict, Any
from difflib import SequenceMatcher

class SemanticVerifier:
    """
    Measures semantic similarity between intent and action
    using multiple techniques: lexical, embedding-simulated, and structural.
    """

    def __init__(self, threshold: float = 0.75):
        self.threshold = threshold

    def score(self, intent_text: str, action_text: str) -> float:
        """
        Compute semantic similarity score between 0.0 and 1.0
        Higher score means better alignment.
        """
        if not intent_text or not action_text:
            return 0.0

        lexical_sim = self._lexical_similarity(intent_text, action_text)
        structural_sim = self._structural_similarity(intent_text, action_text)

        # Weighted combination
        final_score = 0.6 * lexical_sim + 0.4 * structural_sim

        return min(max(final_score, 0.0), 1.0)

    def _lexical_similarity(self, text1: str, text2: str) -> float:
        """Sequence-based similarity using difflib"""
        return SequenceMatcher(None, text1.lower(), text2.lower()).ratio()

    def _structural_similarity(self, intent: str, action: str) -> float:
        """Extract key entities and compare structure"""
        intent_keywords = self._extract_keywords(intent)
        action_keywords = self._extract_keywords(action)

        if not intent_keywords or not action_keywords:
            return 0.0

        common = set(intent_keywords) & set(action_keywords)
        union = set(intent_keywords) | set(action_keywords)

        return len(common) / len(union) if union else 0.0

    def _extract_keywords(self, text: str) -> List[str]:
        """Simple keyword extraction (stopword filtering)"""
        stopwords = {'the', 'a', 'an', 'and', 'or', 'to', 'of', 'for', 'in', 'on', 'at', 'by', 'with', 'without'}
        words = text.lower().split()
        return [w for w in words if w not in stopwords and len(w) > 2]

    def semantic_divergence(self, intent_text: str, action_text: str) -> Dict[str, Any]:
        """
        Returns detailed divergence analysis
        """
        score = self.score(intent_text, action_text)
        return {
            "score": round(score, 4),
            "passed": score >= self.threshold,
            "threshold": self.threshold,
            "lexical_similarity": round(self._lexical_similarity(intent_text, action_text), 4),
            "structural_similarity": round(self._structural_similarity(intent_text, action_text), 4)
        }
