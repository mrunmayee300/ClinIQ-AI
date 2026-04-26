# Benchmarks

## Diagnose Latency

Run:

```bash
python scripts/benchmark_latency.py --base-url http://127.0.0.1:8000/api/v1 --runs 5
```

Outputs:

- Average latency (ms)
- P95 latency (ms)
- Min/Max latency (ms)

Benchmark JSON output is stored at `docs/latency_benchmark.json`.
