from scripts.benchmark_latency import benchmark


if __name__ == "__main__":
    print(benchmark("http://127.0.0.1:8000/api/v1", runs=5))
