import json
import time

from gravit_verifier.engine import EpistemicEngine


def run_benchmarks():
    engine = EpistemicEngine()
    with open("benchmarks/dataset.json") as f:
        dataset = json.load(f)

    correct = 0
    total_time = 0.0

    print(f"Running {len(dataset)} benchmark cases...\n")

    for i, item in enumerate(dataset):
        start = time.perf_counter()
        result = engine.verify(
            intent=item["intent"],
            action=item["action"],
            model_id="benchmark-model"
        )
        duration = time.perf_counter() - start
        total_time += duration

        if result["verdict"] == item.get("label", "ACCEPT"):
            correct += 1
            status = "✅"
        else:
            status = "❌"

        trust = result.get("epistemic_trust_score", 0.0)
        verdict = result.get("verdict", "UNKNOWN")
        print(
            f"{status} Case {i+1}: {verdict} | Trust: {trust:.3f} | "
            f"{duration*1000:.1f}ms"
        )

    accuracy = correct / len(dataset)
    avg_time = total_time / len(dataset)

    print("\n" + "="*60)
    print("BENCHMARK RESULTS")
    print(f"Accuracy: {accuracy:.1%} ({correct}/{len(dataset)})")
    print(f"Avg latency: {avg_time*1000:.1f} ms")
    print(f"Throughput: {1/avg_time:.1f} verifications/sec")
    print("="*60)

if __name__ == "__main__":
    run_benchmarks()
