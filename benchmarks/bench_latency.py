"""
Latency benchmark for epistemic verifier.
"""

import time
import json
import numpy as np
from gravit_verifier.engine import VerificationEngine

def run_latency_benchmark(n=1000):
    engine = VerificationEngine()
    latencies = []

    for _ in range(n):
        start = time.perf_counter()
        engine.verify({
            "agent_id": "bench_agent",
            "action": "transfer",
            "reasoning_chain": ["Step 1", "Step 2"],
            "context": {"balance": 100}
        })
        latencies.append((time.perf_counter() - start) * 1000)

    results = {
        "mean_ms": float(np.mean(latencies)),
        "p50_ms": float(np.percentile(latencies, 50)),
        "p95_ms": float(np.percentile(latencies, 95)),
        "p99_ms": float(np.percentile(latencies, 99))
    }

    print(json.dumps(results, indent=2))
    return results

if __name__ == "__main__":
    run_latency_benchmark()
