import argparse
import json
import time
from pathlib import Path

import requests


DEFAULT_PAYLOAD = {
    "symptoms_text": "Fever, cough, fatigue for 3 days with mild shortness of breath",
    "age": 32,
    "gender": "female",
    "medical_history": ["hypertension"],
    "medications": ["amlodipine"],
    "severity": "moderate",
    "lifestyle": {"smoking": False, "alcohol": False, "activity_level": "moderate"},
}


def benchmark(base_url: str, runs: int = 5) -> dict:
    latencies = []
    for _ in range(runs):
        started = time.perf_counter()
        response = requests.post(f"{base_url}/diagnose", json=DEFAULT_PAYLOAD, timeout=60)
        response.raise_for_status()
        latencies.append((time.perf_counter() - started) * 1000)
    return {
        "runs": runs,
        "avg_ms": round(sum(latencies) / len(latencies), 2),
        "p95_ms": round(sorted(latencies)[int(max(len(latencies) - 1, 0) * 0.95)], 2),
        "min_ms": round(min(latencies), 2),
        "max_ms": round(max(latencies), 2),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", default="http://127.0.0.1:8000/api/v1")
    parser.add_argument("--runs", type=int, default=5)
    parser.add_argument("--out", default="docs/latency_benchmark.json")
    args = parser.parse_args()
    metrics = benchmark(args.base_url, runs=args.runs)
    Path(args.out).write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    main()
