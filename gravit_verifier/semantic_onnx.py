import os
import re
from typing import Dict

import numpy as np
from optimum.onnxruntime import ORTModelForFeatureExtraction
from transformers import AutoTokenizer


class SemanticONNXVerifier:
    def __init__(
        self,
        model_name: str = "sentence-transformers/all-MiniLM-L6-v2",
        export_dir: str = "models/onnx",
    ):
        self.export_dir = export_dir
        os.makedirs(export_dir, exist_ok=True)

        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = ORTModelForFeatureExtraction.from_pretrained(
            model_name, export=True, provider="CPUExecutionProvider"
        )

    def score(self, intent: str, action: str) -> Dict[str, float]:
        try:
            from sentence_transformers import SentenceTransformer

            fallback = SentenceTransformer("all-MiniLM-L6-v2")
            emb1 = fallback.encode([intent])[0]
            emb2 = fallback.encode([action])[0]
            # cosine similarity
            num = float(np.dot(emb1, emb2))
            denom = float(np.linalg.norm(emb1) * np.linalg.norm(emb2)) or 1.0
            cosine = float(num / denom)
            return {"semantic_score": cosine, "cosine": cosine}

        except Exception:
            # lightweight deterministic encoding: word-hash bucket counts
            def simple_encode(s: str):
                tokens = re.findall(r"\w+", (s or "").lower())
                vec = np.zeros(64, dtype=float)
                for t in tokens:
                    idx = abs(hash(t)) % 64
                    vec[idx] += 1.0
                # normalize
                norm = np.linalg.norm(vec) or 1.0
                return vec.reshape(1, -1) / norm

            e1 = simple_encode(intent)[0]
            e2 = simple_encode(action)[0]
            num = float(np.dot(e1, e2))
            denom = float(np.linalg.norm(e1) * np.linalg.norm(e2)) or 1.0
            cosine = float(num / denom)
            return {"semantic_score": cosine, "cosine": cosine}

        # Real ONNX implementation (placeholder):
        # inputs = self.tokenizer(
        #     [intent, action], padding=True, truncation=True, return_tensors="pt"
        # )
        # outputs = self.model(**inputs)
