import json
import logging


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        log_record = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }

        # Include full extra context under "context" if present
        context = getattr(record, "context", None)
        if context:
            log_record["context"] = context

        return json.dumps(log_record)
