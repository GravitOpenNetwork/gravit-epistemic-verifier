from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from typing import Dict


class SemanticVerifier:
    def init(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def score(self, intent: str, action: str) -> Dict[str, float]:
        if not intent or not action:
            return {"cosine": 0.0, "semantic_score": 0.0}

        emb_i = self.model.encode([intent])
        emb_a = self.model.encode([action])
        cosine = float(cosine_similarity(emb_i, emb_a)[0][0])
        keyword_match = sum(1 for w in intent.lower().split() if w in action.lower()) / max(len(intent.split()), 1)
        semantic_score = 0.75 * cosine + 0.25 * keyword_match
        return {
            "cosine": round(cosine, 4),
            "semantic_score": round(min(max(semantic_score, 0.0), 1.0), 4),
        }
