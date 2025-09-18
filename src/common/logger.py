import json
import logging
import sys
from datetime import datetime


class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "timestamp": datetime.utcfromtimestamp(record.created).isoformat() + "Z",
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "line": record.lineno,
        }
        return json.dumps(log_record)


# Common logger for entire app
logger = logging.getLogger("fastapi-chatbot")
logger.setLevel(logging.INFO)

# Stream handler for stdout (Alloy reads this)
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(JSONFormatter())

# Add handler to root logger so uvicorn logs are captured too
logging.getLogger().handlers.clear()
logging.getLogger().addHandler(handler)
logging.getLogger().setLevel(logging.INFO)

logger.addHandler(handler)
