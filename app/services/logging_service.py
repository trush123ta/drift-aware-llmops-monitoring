import json
from datetime import datetime, timezone
from typing import Dict, Any

from app.core.config import settings


class LoggingService:
    def log_request(self, log_data: Dict[str, Any]) -> None:
        settings.LOG_DIR.mkdir(parents=True, exist_ok=True)

        log_data["timestamp"] = datetime.now(timezone.utc).isoformat()

        with open(settings.LOG_FILE, "a", encoding="utf-8") as file:
            file.write(json.dumps(log_data) + "\n")


logging_service = LoggingService()