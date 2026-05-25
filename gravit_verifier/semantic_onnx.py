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
            return fallback.encode([intent]), fallback.encode([action])  # temporary
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

            return simple_encode(intent), simple_encode(action)  # temporary

        # Real ONNX implementation (placeholder):
        # inputs = self.tokenizer(
        #     [intent, action], padding=True, truncation=True, return_tensors="pt"
        # )
        # outputs = self.model(**inputs)
