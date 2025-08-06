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

        # Take the context from the record object and add it to the log record
        context = getattr(record, "context", None)
        if context:
            log_record["context"] = context

        return json.dumps(log_record)
