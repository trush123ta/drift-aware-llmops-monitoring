import json
from pathlib import Path


LOG_FILE = Path("logs/rag_requests.jsonl")


def load_logs():
    if not LOG_FILE.exists():
        return []

    logs = []

    with open(LOG_FILE, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                logs.append(json.loads(line))

    return logs


def analyze_logs():
    logs = load_logs()

    if not logs:
        print("No logs found.")
        return

    total_queries = len(logs)

    avg_latency = sum(log["latency_ms"] for log in logs) / total_queries

    avg_retrieval_distance = sum(
        sum(log["retrieval_distances"]) / len(log["retrieval_distances"])
        for log in logs
    ) / total_queries

    worst_query = max(
        logs,
        key=lambda log: sum(log["retrieval_distances"]) / len(log["retrieval_distances"])
    )

    print("RAG Monitoring Summary")
    print("----------------------")
    print(f"Total queries: {total_queries}")
    print(f"Average latency: {avg_latency:.2f} ms")
    print(f"Average retrieval distance: {avg_retrieval_distance:.4f}")
    print(f"Worst retrieval query: {worst_query['query']}")


if __name__ == "__main__":
    analyze_logs()