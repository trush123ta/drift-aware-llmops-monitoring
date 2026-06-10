import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict


LOG_DIR = Path("logs")
LOG_FILE = LOG_DIR / "rag_requests.jsonl"


def log_rag_request(log_data: Dict[str, Any]) -> None:
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    log_data["timestamp"] = datetime.now(timezone.utc).isoformat()

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(log_data) + "\n")